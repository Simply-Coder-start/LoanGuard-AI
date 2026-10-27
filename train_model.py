import os
from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier

from loan_features import ALL_FEATURES, CATEGORICAL_FEATURES, NUMERIC_FEATURES, engineer_features

ROOT = Path(__file__).resolve().parent
file_path = ROOT / "loan_applications.csv"
if not file_path.exists():
    file_path = ROOT / "sample_loan_applications.csv"

print(f"Loading dataset from: {file_path}")
df = pd.read_csv(file_path)

df = engineer_features(df)
target_col = "fraud_flag"
df = df.dropna(subset=[target_col])

X = df[ALL_FEATURES]
y = df[target_col].astype(int)

test_size = 0.2 if len(df) >= 50 else 0.25
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=42, stratify=y if y.nunique() > 1 else None
)

num_cols = [c for c in ALL_FEATURES if c not in CATEGORICAL_FEATURES]
prep = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), num_cols),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]), CATEGORICAL_FEATURES),
])

model = XGBClassifier(
    n_estimators=250,
    max_depth=5,
    learning_rate=0.03,
    subsample=0.85,
    colsample_bytree=0.85,
    random_state=42,
    eval_metric="logloss",
    n_jobs=4,
)

pipeline = Pipeline([("preprocess", prep), ("model", model)])
pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)
cm = confusion_matrix(y_test, y_pred)

print(f"Accuracy Score: {acc:.4f} ({acc*100:.2f}%)")
print(f"ROC-AUC Score:  {auc:.4f} ({auc*100:.2f}%)")
print("\nConfusion Matrix:\n", cm)
print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

saved_payload = {
    "model": pipeline,
    "features": ALL_FEATURES,
    "numeric_features": num_cols,
    "categorical_features": CATEGORICAL_FEATURES,
    "accuracy": acc,
    "roc_auc": auc,
}
joblib.dump(saved_payload, ROOT / "model.pkl")
print("Model and features saved successfully to 'model.pkl'!")
