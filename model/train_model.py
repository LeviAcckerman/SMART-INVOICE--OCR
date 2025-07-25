# train_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# Path setup
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "invoice_dataset.csv")
DATA_PATH = os.path.abspath(DATA_PATH)

# Load dataset
df = pd.read_csv(DATA_PATH)

# Clean data
df.dropna(subset=['text', 'label'], inplace=True)

# Split data
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Create ML pipeline
model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

# Train model
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "invoice_model.pkl")
joblib.dump(model, MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")
