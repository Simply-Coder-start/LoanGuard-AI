import os
import pandas as pd

file_path = "loan_applications.csv"
if not os.path.exists(file_path):
    if os.path.exists("sample_loan_applications.csv"):
        file_path = "sample_loan_applications.csv"
    elif os.path.exists("archive(2)/loan_applications.csv"):
        file_path = "archive(2)/loan_applications.csv"

print(f"Loading dataset from: {file_path}")
df = pd.read_csv(file_path)

df_cleanable = df.drop(columns=["fraud_type"], errors="ignore")
df_cleaned = df_cleanable.dropna()

print("\n--- First 5 Rows ---")
print(df_cleaned.head())

print("\n--- Column Names ---")
print(list(df_cleaned.columns))

print(f"\nTotal rows before cleaning: {len(df)}")
print(f"Total rows after cleaning: {len(df_cleaned)}")
if "fraud_flag" in df_cleaned.columns:
    print(f"\nFraud distribution:\n{df_cleaned['fraud_flag'].value_counts()}")
