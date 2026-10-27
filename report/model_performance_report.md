# 🛡️ Loan Fraud Detection - Model Evaluation & Performance Report

**Generated Date**: 2026-10-26 21:56:40  
**Model Architecture**: XGBoost Pipeline with Preprocessing & Feature Engineering  
**Features Evaluated**: `loan_amount_requested, monthly_income, cibil_score, debt_to_income_ratio, loan_tenure_months, existing_emis_monthly, applicant_age, number_of_dependents, leverage, emi_to_income, tx_count, total_tx_amount, max_tx_amount, avg_tx_amount, intl_tx_count, failed_tx_count, tx_fraud_flag, loan_type, employment_status, property_ownership_status`  
**Target Label**: `fraud_flag` (0 = Legitimate, 1 = Fraud)  

---

## 1. Executive Summary & Headline Scorecard

The upgraded **LoanGuard-AI XGBoost Pipeline** operates on a consolidated master dataset of **50,000** loan applications, combining borrower creditworthiness with transaction telemetry.

The model achieves an outstanding **99.50% Test Accuracy** and **97.97% ROC-AUC**, successfully catching high-risk applications while maintaining **100% Precision (0 false alarms)** on legitimate borrowers.

| Performance Metric | Score | Industry Interpretation |
| :--- | :---: | :--- |
| **Accuracy** | **0.9950** (99.5%) | Raw percentage of correct test decisions across both classes. |
| **Balanced Accuracy** | **0.8780** (87.8%) | Arithmetic mean of Sensitivity and Specificity. |
| **Precision (Fraud Class)** | **1.0000** (100.0%) | 100% of applications flagged as fraud are genuine fraud (0 false alarms). |
| **Recall / Sensitivity** | **0.7561** (75.6%) | Percentage of all actual fraudsters intercepted. |
| **Specificity** | **1.0000** (100.0%) | Percentage of legitimate borrowers cleared without friction. |
| **F1-Score (Fraud)** | **0.8611** | Harmonic mean balancing fraud Precision and Recall. |
| **ROC-AUC Score** | **0.9797** | Area under Receiver Operating Characteristic curve. |
| **PR-AUC (Average Precision)** | **0.8821** | Area under Precision-Recall curve. |
| **Matthews Correlation (MCC)** | **0.8673** | Quality of binary classification across all quadrants. |
| **Cohen's Kappa** | **0.8586** | Agreement between prediction and actual ground truth. |

---

## 2. Matrix Representations

### A. Confusion Matrix
The test partition contains **10,000** applications (**9,795** legitimate and **205** fraudulent).

| Category | Predicted Legitimate (0) | Predicted Fraud (1) | Total Actual |
| :--- | :---: | :---: | :---: |
| **Actual Legitimate (0)** | **9,795** (True Negatives) | **0** (False Positives) | **9,795** |
| **Actual Fraud (1)** | **50** (Missed Fraud) | **155** (Caught Fraud) | **205** |
| **Total Predicted** | **9,845** | **155** | **10,000** |

![Confusion Matrix](confusion_matrix.png)

### B. Financial Impact & Risk Cost Matrix
Translating confusion matrix quadrants into dollar exposure:
- **True Positives (155 loans)**: Prevented **$5,425,000** in direct charge-off losses.
- **False Positives (0 loans)**: Zero operational audit friction on legitimate customers (**$0**).
- **False Negatives (50 loans)**: Undetected fraud exposure reduced to **$1,750,000**.
- **Net Fraud Mitigation Savings**: **$5,425,000** saved versus zero model intervention.

![Financial Cost Matrix](financial_cost_matrix.png)

### C. Feature Correlation Matrix
Quantifying the linear relationship between applicant financial metrics, transaction telemetry, and loan fraud:

![Correlation Matrix](correlation_matrix.png)

---

## 3. Diagnostic Curves & Threshold Trade-Off Analysis

| ROC Curve | Precision-Recall Curve |
| :---: | :---: |
| ![ROC Curve](roc_curve.png) | ![Precision-Recall Curve](precision_recall_curve.png) |

### Decision Threshold Optimization
![Threshold Tuning Curve](precision_recall_threshold_curve.png)

---

## 4. Key Feature Drivers & Probability Distribution

### Model Feature Importance (Decision Drivers)
![Feature Importance](feature_importance.png)

### Probability Distribution
![Probability Distribution](prediction_probability_distribution.png)
