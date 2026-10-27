"""Compare honest accuracy, fraud-detection, and leakage benchmark models.

The leakage benchmark is intentionally reported separately: loan_status is
derived from the fraud label and must not be used for a real pre-decision
model.
"""

from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "loan_applications.csv"
REPORT_DIR = ROOT / "report"


def score(name, y_true, y_pred, probabilities):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "model": name,
        "accuracy": accuracy_score(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "precision_fraud": precision_score(y_true, y_pred, zero_division=0),
        "recall_fraud": recall_score(y_true, y_pred, zero_division=0),
        "f1_fraud": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, probabilities),
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "true_positives": tp,
    }


def main():
    df = pd.read_csv(DATA_PATH).dropna(subset=["fraud_flag"])
    y = df["fraud_flag"].astype(int)
    train_idx, test_idx = train_test_split(
        df.index, test_size=0.2, random_state=42, stratify=y
    )
    y_train, y_test = y.loc[train_idx], y.loc[test_idx]

    # Honest baseline: maximizes raw accuracy without pretending to detect fraud.
    accuracy_model = DummyClassifier(strategy="most_frequent")
    accuracy_model.fit([[0]] * len(train_idx), y_train)
    accuracy_pred = accuracy_model.predict([[0]] * len(test_idx))
    accuracy_prob = accuracy_model.predict_proba([[0]] * len(test_idx))[:, 1]

    # Honest fraud model: only features available before a loan decision.
    feature_cols = [
        "loan_amount_requested",
        "monthly_income",
        "cibil_score",
        "debt_to_income_ratio",
    ]
    fraud_model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    fraud_model.fit(df.loc[train_idx, feature_cols], y_train)
    fraud_pred = fraud_model.predict(df.loc[test_idx, feature_cols])
    fraud_prob = fraud_model.predict_proba(df.loc[test_idx, feature_cols])[:, 1]

    # Leakage benchmark: loan_status is a post-decision field that directly
    # encodes fraud_flag. It is shown for diagnosis only, never as app input.
    leakage_pred = (df.loc[test_idx, "loan_status"].isin(
        ["Fraudulent - Detected", "Fraudulent - Undetected"]
    )).astype(int).to_numpy()
    leakage_prob = leakage_pred.astype(float)

    rows = [
        score("Raw accuracy baseline (predict legitimate)", y_test, accuracy_pred, accuracy_prob),
        score("Honest fraud model (balanced logistic regression)", y_test, fraud_pred, fraud_prob),
        score("Leakage benchmark (loan_status; invalid for deployment)", y_test, leakage_pred, leakage_prob),
    ]
    result = pd.DataFrame(rows)
    REPORT_DIR.mkdir(exist_ok=True)
    result.to_csv(REPORT_DIR / "model_comparison.csv", index=False)
    result.to_json(REPORT_DIR / "model_comparison.json", orient="records", indent=2)

    print(result.to_string(index=False, float_format=lambda value: f"{value:.4f}"))
    print("\nSaved report/model_comparison.csv and report/model_comparison.json")
    print("\nHonest fraud-model classification report:\n")
    print(classification_report(y_test, fraud_pred, zero_division=0))


if __name__ == "__main__":
    main()
