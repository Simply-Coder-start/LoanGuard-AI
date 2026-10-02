import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Step 1: Load dataset
file_path = "loan_applications.csv"
if not os.path.exists(file_path):
    if os.path.exists("sample_loan_applications.csv"):
        file_path = "sample_loan_applications.csv"
    elif os.path.exists("archive(2)/loan_applications.csv"):
        file_path = "archive(2)/loan_applications.csv"

print(f"Loading dataset from: {file_path}")
df = pd.read_csv(file_path)

# Step 2: Select 4 simple, explainable features and the target
feature_cols = ["loan_amount_requested", "monthly_income", "cibil_score", "debt_to_income_ratio"]
target_col = "fraud_flag"

# Clean any missing values in the selected columns
data = df[feature_cols + [target_col]].dropna()

# Step 3: Separate features (X) and target label (y)
X = data[feature_cols]
y = data[target_col]

# Step 4: Split data into training and test sets
# For small sample runs, adjust test_size safely
test_size = 0.2 if len(data) >= 50 else 0.25
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

# Step 5: Initialize and train the Logistic Regression model
# class_weight='balanced' ensures rare fraud cases receive appropriate weight
model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Step 6: Evaluate the model on test data
y_pred = model.predict(X_test)
print(f"Accuracy Score: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

# Step 7: Save model and feature names to model.pkl
joblib.dump({"model": model, "features": feature_cols}, "model.pkl")
print("Model and features saved successfully to 'model.pkl'!")
