import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ==========================
# Load Dataset
# ==========================

df = pd.read_csv(
    "processed_data/amazon_reviews_cleaned.csv"
)

print("Dataset Shape:", df.shape)

# ==========================
# Feature Engineering
# ==========================

df["combined_text"] = (
    df["Summary"].fillna("").astype(str)
    + " "
    + df["Text"].fillna("").astype(str)
)

X = df["combined_text"]
y = df["Score"]

# ==========================
# Train/Test Split
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==========================
# TF-IDF Vectorization
# ==========================

vectorizer = TfidfVectorizer(
    max_features=10000,
    stop_words="english"
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ==========================
# Model
# ==========================

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

# ==========================
# Training
# ==========================

print("\nTraining Model...\n")

model.fit(
    X_train_vec,
    y_train
)

# ==========================
# Predictions
# ==========================

predictions = model.predict(
    X_test_vec
)

# ==========================
# Evaluation
# ==========================

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        predictions
    )
)

# ==========================
# Save Model
# ==========================

joblib.dump(
    model,
    "models/best_rating_model.pkl"
)

joblib.dump(
    vectorizer,
    "models/tfidf_vectorizer.pkl"
)

print("\nModel Saved:")
print("models/best_rating_model.pkl")

print("\nVectorizer Saved:")
print("models/tfidf_vectorizer.pkl")