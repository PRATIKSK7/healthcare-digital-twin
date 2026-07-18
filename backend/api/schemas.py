from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TelemetryData(BaseModel):
    patient_id: str
    
    # Demographics
    age: int
    gender: str
    bmi: float
    
    # Vitals
    heart_rate: int
    blood_pressure_sys: int
    blood_pressure_dia: int
    spO2: float
    respiratory_rate: int
    temperature: float
    blood_glucose: float
    
    # Symptom Details
    symptoms: List[str] = []
    symptom_duration_days: int = 0
    symptom_severity: int = 1
    
    # Habits & Lifestyle
    smoking: bool = False
    alcohol: bool = False
    lifestyle: str = "Sedentary"
    
    # Medical Background
    comorbidities: List[str] = []
    medical_history: List[str] = []
    family_history: List[str] = []
    previous_diseases: List[str] = []
    current_medication: List[str] = []
    vaccination_history: List[str] = []
    
    # Other
    pregnancy: bool = False
    
    timestamp: Optional[str] = None

class PatientSyncResponse(BaseModel):
    status: str
    message: str
    patient_id: str

class TwinStateResponse(BaseModel):
    patient_id: str
    current_vitals: Dict[str, Any]
    baseline_deviation: float
    last_updated: str

class RiskPredictionRequest(BaseModel):
    patient_id: str
    telemetry: Optional[TelemetryData] = None
    include_explanation: bool = False

class DiseasePrediction(BaseModel):
    disease: str
    probability: float

class RiskPredictionResponse(BaseModel):
    patient_id: str
    severity_score: float
    priority: str
    estimated_wait_time: str
    confidence: float
    top_shap_contributors: Optional[List[Dict[str, str]]] = None

class BatchPredictionRequest(BaseModel):
    patients: List[RiskPredictionRequest]

class BatchPredictionResponse(BaseModel):
    results: List[RiskPredictionResponse]
    processing_time_ms: Optional[float] = None

class TreatmentSimulationRequest(BaseModel):
    patient_id: str
    telemetry: Optional[TelemetryData] = None
    intervention: str
    dosage: Optional[str] = None
    duration_days: int = 1

class OrganHealth(BaseModel):
    heart: str
    lungs: str
    kidneys: str
    liver: str

class TreatmentResponse(BaseModel):
    efficacy_score: float
    side_effects: List[str]
    interaction_warnings: List[str]

class TreatmentSimulationResponse(BaseModel):
    patient_id: str
    intervention: str
    projected_vitals: Dict[str, Any]
    disease_progression: str
    treatment_response: TreatmentResponse
    recovery_timeline_days: int
    organ_health: OrganHealth
    medication_effects: Dict[str, Any]
    expected_risk_level: str
    improvement_score: float

# Frontend specific schemas
class FrontendPredictRequest(BaseModel):
    age: int
    gender: str
    symptoms: List[str]
    hr: Optional[int] = 75
    sbp: Optional[int] = 120
    smoking: Optional[bool] = False
    symptom_duration_days: Optional[int] = 5
    symptom_severity: Optional[int] = 5
    spo2: Optional[float] = 98.0
    temp: Optional[float] = 37.0
    respiratory_rate: Optional[int] = 16
    glucose: Optional[float] = 100.0

class FeatureExplanation(BaseModel):
    feature: str
    contribution: str

class FrontendTriageResponse(BaseModel):
    severity_score: float
    priority_category: str
    waiting_priority: str
    initial_clinical_risk: str
    confidence: float
    explanations: Optional[List[FeatureExplanation]] = []

class FrontendSimulateRequest(BaseModel):
    name: str
    age: int
    gender: str
    symptoms: List[str]
    hr: int
    sbp: int
    dbp: int
    temp: float
    spo2: int
    glucose: int
    bmi: float
    crp: float
    scenario: str

class FrontendSimulateResponse(BaseModel):
    overallRisk: str
    primaryCondition: str
    organSystems: List[Dict[str, Any]]
    vitalStatus: List[Dict[str, Any]]
    timeline: List[Dict[str, str]]
    narrative: str
    recommendations: List[str]
    projectedTrends: Dict[str, Any]
    stats: List[Dict[str, str]]

