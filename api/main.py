import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Define the input data schema using Pydantic
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Initialize the FastAPI app
app = FastAPI(title="Iris Species Predictor API")

# Load the trained model from the file
# The model.joblib file will be copied into the Docker image
try:
    model = joblib.load("model.joblib")
except FileNotFoundError:
    model = None # Handle case where model is not found

@app.on_event("startup")
def startup_event():
    if model is None:
        raise RuntimeError("Model 'model.joblib' could not be loaded. Ensure it's in the 'api/' directory.")
    print("Model loaded successfully!")

@app.get("/", tags=["General"])
def read_root():
    """Returns a welcome message."""
    return {"message": "Welcome to the Iris Prediction API!"}

@app.get("/health", tags=["General"])
def health_check():
    """Health check endpoint for Kubernetes probes."""
    return {"status": "ok"}

@app.post("/predict", tags=["Prediction"])
def predict_species(data: IrisFeatures):
    """Predicts the iris species from input features."""
    # Create a DataFrame from the input data
    input_df = pd.DataFrame([data.dict()])
    
    # Make a prediction
    prediction = model.predict(input_df)[0]
    
    return {"predicted_species": prediction}
