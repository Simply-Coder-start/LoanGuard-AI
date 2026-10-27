import pandas as pd

NUMERIC_FEATURES = [
    "loan_amount_requested",
    "monthly_income",
    "cibil_score",
    "debt_to_income_ratio",
    "loan_tenure_months",
    "existing_emis_monthly",
    "applicant_age",
    "number_of_dependents",
    "leverage",
    "emi_to_income",
    "tx_count",
    "total_tx_amount",
    "max_tx_amount",
    "avg_tx_amount",
    "intl_tx_count",
    "failed_tx_count",
    "tx_fraud_flag",
]

CATEGORICAL_FEATURES = [
    "loan_type",
    "employment_status",
    "property_ownership_status",
]

ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def engineer_features(frame: pd.DataFrame) -> pd.DataFrame:
    df = frame.copy()
    if "loan_amount_requested" in df.columns and "monthly_income" in df.columns:
        df["leverage"] = df["loan_amount_requested"] / (df["monthly_income"] * 12.0 + 1.0)
    else:
        df["leverage"] = 0.0

    if "existing_emis_monthly" in df.columns and "monthly_income" in df.columns:
        df["emi_to_income"] = df["existing_emis_monthly"] / (df["monthly_income"] + 1.0)
    else:
        df["emi_to_income"] = 0.0

    for col in NUMERIC_FEATURES:
        if col not in df.columns:
            df[col] = 0.0

    for col in CATEGORICAL_FEATURES:
        if col not in df.columns:
            df[col] = "Other"

    return df
