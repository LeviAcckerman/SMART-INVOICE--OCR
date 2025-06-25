import joblib
import os

# Load model only once when the file is imported
MODEL_PATH = os.path.join("model", "invoice_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"[ERROR] Failed to load model: {e}")
    model = None

def classify_invoice(text):
    """
    Classify the invoice text into a category (e.g., Retail, Utility).
    
    :param text: Raw OCR invoice text
    :return: Predicted category or error message
    """
    if model is None:
        return "[ERROR] Model not loaded."

    try:
        prediction = model.predict([text])[0]
        return prediction
    except Exception as e:
        return f"[ERROR] Classification failed: {e}"
