import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib 
import os

# Load the dataset
dataset_path = os.path.join("dataset", "invoice_dataset.csv")

try:
    df = pd.read_csv(dataset_path)

    # Make sure required columns exist
    if 'text' not in df.columns or 'label' not in df.columns:
        raise ValueError("CSV must contain 'text' and 'label' columns")

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['label'], test_size=0.2, random_state=42
    )

    # Create a pipeline: TF-IDF + Naive Bayes
    model = make_pipeline(
        TfidfVectorizer(),
        MultinomialNB()
    )

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate
    accuracy = model.score(X_test, y_test)
    print(f"Model trained with accuracy: {accuracy:.2f}")

    # Save the model
    model_path = os.path.join("model", "invoice_model.pkl")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

except Exception as e:
    print(f"[ERROR] Training failed: {e}")
