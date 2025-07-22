import joblib
import os

MODEL_PATH = os.path.join("model", "invoice_model.pkl")

def load_model():
    """Load and return the trained ML model."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def predict_category(text):
    """Predict the category of the invoice using the trained model."""
    model = load_model()
    return model.predict([text])[0]
