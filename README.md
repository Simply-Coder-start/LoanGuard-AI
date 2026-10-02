# 🛡️ LoanGuard-AI: Loan Fraud Detection & Risk Analysis

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Model-F7931E.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**LoanGuard-AI** is a minimalist, highly explainable machine learning system designed to detect high-risk and potentially fraudulent loan applications in real time. Built with **Scikit-Learn (Logistic Regression)** and **Streamlit**, it provides credit underwriters and applicants with transparent risk scores and plain-English factor breakdowns.

---

## 🚀 Key Features

- **⚡ Instant Fraud Risk Scoring:** Generates an intuitive **Fraud Risk Score (0% – 100%)** calibrated for financial underwriting.
- **🔍 Explainable Decision Drivers:** Breaks down the underlying causes of risk (excessive debt-to-income, subprime credit history, high loan leverage).
- **🖥️ Minimalist Web Interface:** Clean, reactive Streamlit dashboard with zero unnecessary complexity.
- **🧪 Out-of-the-Box Ready:** Includes a pre-trained model (`model.pkl`) and sample dataset (`sample_loan_applications.csv`) for immediate local testing.

---

## 📁 Repository Structure

```text
├── app.py                         # Streamlit interactive web application
├── data_cleaning.py               # Data loading, inspection, and cleaning script
├── train_model.py                 # Standalone model training and export script
├── model_training.ipynb           # Step-by-step Jupyter Notebook with beginner explanations
├── model.pkl                      # Serialized trained model & feature list
├── sample_loan_applications.csv   # Sample dataset for instant out-of-the-box runs
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation
```

---

## 🛠️ Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Simply-Coder-start/LoanGuard-AI.git
cd LoanGuard-AI
```

### 2. Set Up a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Running the Application

### Launch the Streamlit Web App
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### (Optional) Retrain the Model
To re-fit the Logistic Regression model:
```bash
python train_model.py
```
Or explore the interactive notebook:
```bash
jupyter notebook model_training.ipynb
```

---

## 📊 Dataset & Model Architecture

- **Dataset:** Modeled after the Kaggle *Loan Application & Transaction Fraud Detection* benchmark.
- **Model:** Logistic Regression with `class_weight='balanced'` to effectively handle severe class imbalance in real-world fraud scenarios (~2% fraud incidence).
- **Core Features Evaluated:**
  1. `loan_amount_requested`: Principal loan amount applied for.
  2. `monthly_income`: Verified applicant monthly earnings.
  3. `cibil_score`: Credit / CIBIL score (300–900).
  4. `debt_to_income_ratio`: Ratio of existing monthly debt obligations to income.

---

## 🔒 Security & Privacy

This repository excludes all raw private datasets, environment secrets, and local machine configurations. A standardized `.gitignore` is provided to protect proprietary data and ensure lightweight repository distribution.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
