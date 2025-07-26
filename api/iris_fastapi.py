import os
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Define the input data schema using Pydantic
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Initialize the FastAPI app
app = FastAPI(title="Iris Classifier API")

# Load the trained model from the file
model_path = "model.joblib"
model = None

@app.on_event("startup")
def load_model():
    """Load the model at startup."""
    global model
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print("Model loaded successfully!")
    else:
        print(f"Warning: Model file not found at {model_path}")


@app.get("/", tags=["General"])
def read_root():
    """Returns a welcome message."""
    return {"message": "Welcome to the Iris Classifier API!"}

@app.get("/health", tags=["General"])
def health_check():
    """Health check endpoint for Kubernetes probes."""
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict/", tags=["Prediction"])
def predict_species(data: IrisInput):
    """Predicts the iris species from input features."""
    if model is None:
        return {"error": "Model is not loaded. Cannot make predictions."}
        
    # Create a DataFrame from the input data
    input_df = pd.DataFrame([data.dict()])
    
    # Make a prediction
    prediction = model.predict(input_df)[0]
    
    return {"predicted_class": prediction}
