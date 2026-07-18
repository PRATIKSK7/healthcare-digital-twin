from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from api.routes import router as api_router
from models.manager import model_manager
from core.security import limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import time
import logging
from contextlib import asynccontextmanager

# Configure structured logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing global ModelManager...")
    _ = model_manager
    yield
    logger.info("Shutting down application...")

app = FastAPI(
    title="Healthcare Digital Twin API",
    version="1.0.0",
    description="Production-Ready Medical Forecasting API",
    lifespan=lifespan
)

# Attach Rate Limiter
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded. Try again later."})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error for {request.url}: {exc.errors()}")
    return JSONResponse(status_code=422, content={"detail": "Invalid payload format.", "errors": exc.errors()})

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error. Please contact support."})

# Global Profiling Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    process_time_ms = round(process_time * 1000, 2)
    response.headers["X-Process-Time"] = f"{process_time_ms} ms"
    if process_time_ms > 100:
        logger.info(f"[{request.method}] {request.url.path} completed in {process_time_ms}ms")
    return response

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Healthcare Digital Twin API", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
