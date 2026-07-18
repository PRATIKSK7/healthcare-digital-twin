import asyncio
import json
import hashlib
from typing import Dict, Any, List
from cachetools import LRUCache
from models.inference import predict_triage_severity
import os
import joblib
import logging
import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class ModelManager:
    """
    Singleton class for thread-safe model execution and caching.
    Ensures the model is loaded exactly once and leverages an LRU cache
    to return identical inference requests instantly (<1ms).
    """
    _instance = None
    _lock = asyncio.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            # Capacity for 10,000 unique inference results
            self.cache = LRUCache(maxsize=10000)
            self._initialized = True
            
            self.model = None
            self.preprocessor = None
            self.metadata = {
                "version": "unknown",
                "status": "not_loaded",
                "timestamp": "unknown",
                "error": None
            }
            
            self._load_latest_model()
            
            if self.model:
                logger.info("🚀 Global ModelManager Initialized (LRU Cache active). ML Model Loaded successfully.")
            else:
                logger.error("❌ Global ModelManager Initialized but failed to load ML model.")

    def _load_latest_model(self):
        try:
            from catboost import CatBoostRegressor
            import json
            
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # This is 'backend/'
            models_dir = os.path.join(base_dir, "models")
            
            model_path = os.path.join(models_dir, "catboost_triage_v2.cbm")
            preprocessor_path = os.path.join(models_dir, "preprocessor.joblib")
            feature_list_path = os.path.join(models_dir, "feature_list.json")
            metadata_path = os.path.join(models_dir, "model_metadata.json")
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Missing {model_path}")
                
            logger.info(f"Loading CatBoost model...")
            self.model = CatBoostRegressor().load_model(model_path)
            self.preprocessor = joblib.load(preprocessor_path)
            
            with open(feature_list_path, 'r') as f:
                self.feature_list = json.load(f)
                
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
                
            self.metadata["version"] = "catboost_v2"
            self.metadata["status"] = "loaded"
            self.metadata["timestamp"] = os.path.getmtime(model_path)
                
        except Exception as e:
            self.metadata["status"] = "error"
            self.metadata["error"] = str(e)
            logger.error(f"Failed to load latest model: {e}")
            
    def _generate_cache_key(self, patient_data: Dict[str, Any]) -> str:
        """Deterministically hashes the payload to use as a fast cache key."""
        # Ensure consistent ordering for reliable hashing
        canonical = json.dumps(patient_data, sort_keys=True)
        return hashlib.md5(canonical.encode('utf-8')).hexdigest()

    async def predict_async(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Async inference with LRU caching and thread-safe lock."""
        cache_key = self._generate_cache_key(patient_data)
        
        # 1. Check Cache
        if cache_key in self.cache:
            # print("⚡ Cache Hit! Returning instantly.")
            return self.cache[cache_key]

        # 2. Thread-Safe Execution
        async with self._lock:
            if not self.model or not self.preprocessor:
                raise RuntimeError(f"ML Model not loaded. Reason: {self.metadata.get('error')}")
                
            # For CPU-bound ML tasks, to_thread prevents blocking the FastAPI event loop
            result = await asyncio.to_thread(
                predict_triage_severity, 
                patient_data, 
                self.model, 
                self.preprocessor, 
                self.feature_list,
                True # include_explanation
            )
            
            # Save to cache
            self.cache[cache_key] = result
            return result

    async def predict_batch_async(self, batch_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Handles multiple predictions efficiently using async gather."""
        tasks = [self.predict_async(patient_data) for patient_data in batch_data]
        results = await asyncio.gather(*tasks)
        return list(results)

# Global singleton instance
model_manager = ModelManager()
