from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

# Initialize the FastAPI app
app = FastAPI(title="Iris Classifier API")

# Define the path to the model file using an environment variable for flexibility
MODEL_FILE_PATH = os.getenv("MODEL_PATH", "model.joblib")
model = None

@app.on_event("startup")
def load_model():
    """
    Load the model during startup. This is more robust than loading at the global scope.
    """
    global model
    if os.path.exists(MODEL_FILE_PATH):
        model = joblib.load(MODEL_FILE_PATH)
        print(f"✅ Model loaded successfully from {MODEL_FILE_PATH}")
    else:
        print(f"❌ WARNING: Model file not found at {MODEL_FILE_PATH}")

# Define the input data schema using Pydantic
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def root():
    """
    Root endpoint to welcome users to the API.
    """
    return {"message": "Welcome to the Iris Classifier API!"}

@app.get("/health", status_code=200)
def health_check():
    """
    Health check endpoint for Kubernetes probes.
    Returns a 200 OK status if the API is running.
    """
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict/")
def predict(data: IrisInput):
    """
    Takes Iris flower features as input and returns the predicted species.
    """
    if model is None:
        return {"error": "Model is not loaded. Cannot make predictions."}
        
    # Convert input data into a pandas DataFrame
    df = pd.DataFrame([data.dict()])
    
    # Make a prediction using the loaded model
    prediction = model.predict(df)[0]
    
    # Return the prediction in a JSON response
    return {"predicted_class": prediction}
