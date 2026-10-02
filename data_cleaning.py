import os
import pandas as pd

# 1. Locate dataset file
file_path = "loan_applications.csv"
if not os.path.exists(file_path):
    if os.path.exists("sample_loan_applications.csv"):
        file_path = "sample_loan_applications.csv"
    elif os.path.exists("archive(2)/loan_applications.csv"):
        file_path = "archive(2)/loan_applications.csv"

print(f"Loading dataset from: {file_path}")
df = pd.read_csv(file_path)

# 2. 'fraud_type' is empty (NaN) for non-fraud cases because legitimate loans have no fraud category.
# Drop 'fraud_type' before dropping missing rows so we retain both fraud and legitimate applications.
df_cleanable = df.drop(columns=["fraud_type"], errors="ignore")
df_cleaned = df_cleanable.dropna()

# 3. Show the first 5 rows
print("\n--- First 5 Rows ---")
print(df_cleaned.head())

# 4. List all column names
print("\n--- Column Names ---")
print(list(df_cleaned.columns))

print(f"\nTotal rows before cleaning: {len(df)}")
print(f"Total rows after cleaning: {len(df_cleaned)}")
if "fraud_flag" in df_cleaned.columns:
    print(f"\nFraud distribution:\n{df_cleaned['fraud_flag'].value_counts()}")
