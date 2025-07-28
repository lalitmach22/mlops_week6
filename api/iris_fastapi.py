import os
import joblib
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException, Response, status
from fastapi.responses import JSONResponse
import logging
import time
import json

# OpenTelemetry imports for tracing
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter

# --- Observability Setup ---

# 1. Setup Tracer for Google Cloud Trace
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(CloudTraceSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# 2. Setup structured JSON logging for Google Cloud Logging
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record, self.datefmt),
        }
        if isinstance(record.msg, dict):
            log_record.update(record.msg)
        return json.dumps(log_record)

logger = logging.getLogger("iris-classifier")
logger.setLevel(logging.INFO)
if logger.hasHandlers():
    logger.handlers.clear()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)

# --- FastAPI Application ---

app = FastAPI(title="Iris Classifier API")

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

model_path = "model.joblib"
model = None
app_state = {"is_ready": False, "is_alive": True}

@app.on_event("startup")
async def startup_event():
    """Load the model and set app state at startup."""
    global model
    logger.info({"event": "startup_begin", "message": "Starting model loading process..."})
    time.sleep(1)
    logger.info({"event": "startup_check", "message": f"Checking for model at: {model_path}"})
    
    if os.path.exists(model_path):
        try:
            logger.info({"event": "model_loading", "message": "Loading model from disk..."})
            model = joblib.load(model_path)
            app_state["is_ready"] = True
            logger.info({"event": "startup_success", "message": "Model loaded successfully.", "model_type": str(type(model))})
        except Exception as e:
            app_state["is_ready"] = False
            logger.error({"event": "model_load_error", "message": f"Failed to load model: {str(e)}"})
    else:
        app_state["is_ready"] = False
        logger.error({"event": "startup_failure", "message": f"Model file not found at {model_path}"})
        
    logger.info({"event": "startup_complete", "message": f"Startup completed. Ready state: {app_state['is_ready']}"})

# --- Health Probes ---

@app.get("/live_check", tags=["Probes"])
async def liveness_probe():
    if app_state["is_alive"]:
        return {"status": "alive", "timestamp": time.time()}
    logger.warning({"event": "liveness_failure", "message": "Liveness check failed"})
    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/ready_check", tags=["Probes"])
async def readiness_probe():
    if app_state["is_ready"]:
        return {"status": "ready", "model_loaded": model is not None, "timestamp": time.time()}
    logger.warning({"event": "readiness_failure", "message": f"Readiness check failed. Ready: {app_state['is_ready']}, Model: {model is not None}"})
    return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

# --- Middleware & Exception Handling ---

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = round((time.time() - start_time) * 1000, 2)
    response.headers["X-Process-Time-ms"] = str(duration)
    return response

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    span = trace.get_current_span()
    trace_id = format(span.get_span_context().trace_id, "032x") if span.is_recording() else "not_recording"
    
    logger.error({
        "event": "unhandled_exception",
        "trace_id": trace_id,
        "path": str(request.url),
        "error": str(exc)
    })
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "trace_id": trace_id},
    )

# --- API Endpoints ---

@app.get("/", tags=["General"])
def read_root():
    return {"message": "Welcome to the Iris Classifier API with Observability!"}

@app.post("/predict/", tags=["Prediction"])
def predict_species(data: IrisInput):
    with tracer.start_as_current_span("model_inference") as span:
        trace_id = format(span.get_span_context().trace_id, "032x")
        
        if not app_state["is_ready"] or model is None:
            logger.warning({
                "event": "prediction_failure",
                "trace_id": trace_id,
                "reason": "Model not ready"
            })
            raise HTTPException(status_code=503, detail="Model is not ready.")
            
        try:
            input_df = pd.DataFrame([data.dict()])
            start_time = time.time()
            prediction = model.predict(input_df)[0]
            latency = round((time.time() - start_time) * 1000, 2)
            
            logger.info({
                "event": "prediction_success",
                "trace_id": trace_id,
                "input": data.dict(),
                "result": prediction,
                "latency_ms": latency
            })
            return {"predicted_class": prediction}

        except Exception as e:
            logger.error({
                "event": "prediction_error",
                "trace_id": trace_id,
                "error": str(e)
            })
            raise HTTPException(status_code=500, detail="Prediction failed during model inference.")
