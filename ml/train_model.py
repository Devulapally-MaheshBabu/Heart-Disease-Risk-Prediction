"""
Heart Disease Risk Predictor - Model Training
Dataset: UCI Cleveland Heart Disease Dataset (via sklearn/fetch)
"""

import pandas as pd
import numpy as np
import pickle
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, roc_auc_score
)
from sklearn.pipeline import Pipeline

# ─────────────────────────────────────────────
# 1. Load Dataset
# ─────────────────────────────────────────────
# Using the Cleveland Heart Disease dataset from UCI (via URL)
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"

columns = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal", "target"
]

print("Loading dataset...")
df = pd.read_csv(url, names=columns, na_values="?")

# ─────────────────────────────────────────────
# 2. Preprocessing
# ─────────────────────────────────────────────
print(f"Dataset shape: {df.shape}")
print(f"Missing values:\n{df.isnull().sum()}")

# Drop rows with missing values (only 6 rows)
df.dropna(inplace=True)

# Binarize target: 0 = no disease, 1 = disease (original values 1-4)
df["target"] = (df["target"] > 0).astype(int)

print(f"\nTarget distribution:\n{df['target'].value_counts()}")

# Features and label
X = df.drop("target", axis=1)
y = df["target"]

feature_names = list(X.columns)

# ─────────────────────────────────────────────
# 3. Train/Test Split
# ─────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTraining samples: {len(X_train)}, Test samples: {len(X_test)}")

# ─────────────────────────────────────────────
# 4. Build Pipeline (Scaler + Model)
# ─────────────────────────────────────────────
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        min_samples_split=5,
        random_state=42,
        class_weight="balanced"
    ))
])

# ─────────────────────────────────────────────
# 5. Train
# ─────────────────────────────────────────────
print("\nTraining model...")
pipeline.fit(X_train, y_train)

# ─────────────────────────────────────────────
# 6. Evaluate
# ─────────────────────────────────────────────
y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
roc_auc  = roc_auc_score(y_test, y_prob)
cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")

print("\n" + "="*50)
print("MODEL EVALUATION")
print("="*50)
print(f"Accuracy  : {accuracy:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")
print(f"CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["No Disease", "Disease"]))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ─────────────────────────────────────────────
# 7. Save Model + Metadata
# ─────────────────────────────────────────────
with open("model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

metadata = {
    "feature_names": feature_names,
    "accuracy": round(accuracy, 4),
    "roc_auc": round(roc_auc, 4),
    "cv_accuracy_mean": round(cv_scores.mean(), 4),
    "cv_accuracy_std": round(cv_scores.std(), 4),
    "model_type": "RandomForestClassifier",
    "n_estimators": 100
}

with open("model_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("\n✅ Model saved to model.pkl")
print("✅ Metadata saved to model_metadata.json")