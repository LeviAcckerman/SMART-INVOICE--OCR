import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Load the dataset
df = pd.read_csv('../dataset/invoice_dataset.csv')

# Drop rows with missing values
df.dropna(subset=['text', 'label'], inplace=True)

# Check class distribution
label_counts = df['label'].value_counts()
print("Label distribution:\n", label_counts)

# Drop labels that have less than 2 samples (not suitable for stratified split)
valid_labels = label_counts[label_counts >= 2].index
df = df[df['label'].isin(valid_labels)]

# If still not enough data, raise an error
if df['label'].nunique() < 2:
    raise ValueError("Need at least 2 classes with at least 2 samples each for training.")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['label'], test_size=0.2, random_state=42, stratify=df['label']
)

# Create a pipeline: TF-IDF vectorizer + Multinomial Naive Bayes classifier
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', MultinomialNB())
])

# Train the model
model_pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = model_pipeline.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the model in the current folder as invoice_model.pkl
joblib.dump(model_pipeline, 'invoice_model.pkl')
print("Model saved to: invoice_model.pkl")
