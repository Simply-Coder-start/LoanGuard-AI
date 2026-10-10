"""
Comprehensive Model Evaluation & Report Generation Script
Generates all matrix representations, diagnostic curves, precision/accuracy threshold tables,
and saves high-resolution charts and metric data to the 'report/' directory.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    roc_curve,
    precision_recall_curve,
    confusion_matrix,
    classification_report,
    matthews_corrcoef,
    cohen_kappa_score,
    log_loss,
    brier_score_loss
)
from sklearn.calibration import calibration_curve
import joblib

# Set professional plotting aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

def generate_all_reports():
    # Detect project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(current_dir) == "report_generation":
        base_dir = os.path.dirname(current_dir)
    else:
        base_dir = current_dir

    # 1. Create report folder in project root
    report_dir = os.path.join(base_dir, "report")
    os.makedirs(report_dir, exist_ok=True)
    print(f"[1/8] Ensuring report directory exists: '{report_dir}/'")

    # 2. Locate and load dataset
    possible_paths = [
        os.path.join(base_dir, "loan_applications.csv"),
        "loan_applications.csv",
        os.path.join(base_dir, "sample_loan_applications.csv"),
        "sample_loan_applications.csv",
        os.path.join(base_dir, "archive(2)", "loan_applications.csv"),
        "archive(2)/loan_applications.csv"
    ]
    file_path = next((p for p in possible_paths if os.path.exists(p)), None)
    if not file_path:
        raise FileNotFoundError("Could not find loan dataset file.")

    print(f"[2/8] Loading dataset from '{file_path}'...")
    df = pd.read_csv(file_path)

    feature_cols = ["loan_amount_requested", "monthly_income", "cibil_score", "debt_to_income_ratio"]
    target_col = "fraud_flag"

    data = df[feature_cols + [target_col]].dropna()
    X = data[feature_cols]
    y = data[target_col]

    # 3. Train-Test split (stratified for class imbalance)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 4. Train Model
    print("[3/8] Training Logistic Regression model with balanced class weights...")
    model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    # Persist model.pkl
    model_path = os.path.join(base_dir, "model.pkl")
    joblib.dump({"model": model, "features": feature_cols}, model_path)

    # Predictions & Probabilities
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # 5. Compute Full Suite of Precision Scores, Accuracy, and Classification Metrics
    print("[4/8] Computing precision, recall, accuracy, and discrimination metrics...")
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    accuracy = float(accuracy_score(y_test, y_pred))
    balanced_acc = float(balanced_accuracy_score(y_test, y_pred))
    precision_1 = float(precision_score(y_test, y_pred, zero_division=0))
    recall_1 = float(recall_score(y_test, y_pred, zero_division=0))
    specificity = float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0
    f1_1 = float(f1_score(y_test, y_pred, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, y_proba))
    pr_auc = float(average_precision_score(y_test, y_proba))
    mcc = float(matthews_corrcoef(y_test, y_pred))
    kappa = float(cohen_kappa_score(y_test, y_pred))
    loss_val = float(log_loss(y_test, y_proba))
    brier = float(brier_score_loss(y_test, y_proba))

    # Threshold analysis
    thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    thresh_records = []
    for t in thresholds:
        preds_t = (y_proba >= t).astype(int)
        cm_t = confusion_matrix(y_test, preds_t)
        tn_t, fp_t, fn_t, tp_t = cm_t.ravel()
        p_t = precision_score(y_test, preds_t, zero_division=0)
        r_t = recall_score(y_test, preds_t, zero_division=0)
        f1_t = f1_score(y_test, preds_t, zero_division=0)
        acc_t = accuracy_score(y_test, preds_t)
        thresh_records.append({
            "threshold": t,
            "accuracy": round(float(acc_t), 4),
            "precision": round(float(p_t), 4),
            "recall": round(float(r_t), 4),
            "f1_score": round(float(f1_t), 4),
            "true_positives": int(tp_t),
            "false_positives": int(fp_t),
            "true_negatives": int(tn_t),
            "false_negatives": int(fn_t)
        })
    thresh_df = pd.DataFrame(thresh_records)
    thresh_df.to_csv(os.path.join(report_dir, "threshold_analysis.csv"), index=False)

    # Classification report
    clf_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    clf_df = pd.DataFrame(clf_dict).transpose()
    clf_df.to_csv(os.path.join(report_dir, "classification_report.csv"))

    with open(os.path.join(report_dir, "classification_report.txt"), "w") as f:
        f.write(classification_report(y_test, y_pred, zero_division=0))

    # Metrics summary JSON & CSV
    metrics_summary = {
        "dataset_statistics": {
            "total_samples": int(len(data)),
            "test_samples": int(len(y_test)),
            "fraud_prevalence_pct": round(float(y.mean() * 100), 2),
            "test_fraud_cases": int(y_test.sum()),
            "test_legitimate_cases": int((y_test == 0).sum())
        },
        "headline_metrics": {
            "accuracy": round(accuracy, 4),
            "balanced_accuracy": round(balanced_acc, 4),
            "precision_fraud": round(precision_1, 4),
            "recall_fraud_sensitivity": round(recall_1, 4),
            "specificity": round(specificity, 4),
            "f1_score_fraud": round(f1_1, 4),
            "roc_auc_score": round(roc_auc, 4),
            "pr_auc_average_precision": round(pr_auc, 4),
            "matthews_correlation_coefficient": round(mcc, 4),
            "cohens_kappa": round(kappa, 4),
            "log_loss": round(loss_val, 4),
            "brier_score": round(brier, 4)
        },
        "confusion_matrix_breakdown": {
            "true_positives_caught_fraud": int(tp),
            "false_positives_false_alarms": int(fp),
            "true_negatives_correct_legitimate": int(tn),
            "false_negatives_missed_fraud": int(fn)
        },
        "decision_threshold_recommendations": {
            "standard_threshold_0_5": {
                "precision": round(precision_1, 4),
                "recall": round(recall_1, 4),
                "f1_score": round(f1_1, 4)
            },
            "high_recall_conservative_threshold_0_3": next(r for r in thresh_records if r["threshold"] == 0.3),
            "high_precision_selective_threshold_0_7": next(r for r in thresh_records if r["threshold"] == 0.7)
        }
    }

    with open(os.path.join(report_dir, "metrics_summary.json"), "w") as f:
        json.dump(metrics_summary, f, indent=4)

    metrics_df = pd.DataFrame([
        {"Metric": "Accuracy", "Value": accuracy, "Description": "Overall correct predictions percentage (can be biased by class imbalance)"},
        {"Metric": "Balanced Accuracy", "Value": balanced_acc, "Description": "Mean of Sensitivity (Recall) and Specificity"},
        {"Metric": "Precision (Fraud)", "Value": precision_1, "Description": "Proportion of flagged loans that are actual fraud (TP / (TP + FP))"},
        {"Metric": "Recall / Sensitivity (Fraud)", "Value": recall_1, "Description": "Proportion of actual fraud captured by model (TP / (TP + FN))"},
        {"Metric": "Specificity", "Value": specificity, "Description": "Proportion of legitimate loans accurately cleared (TN / (TN + FP))"},
        {"Metric": "F1-Score (Fraud)", "Value": f1_1, "Description": "Harmonic mean of Precision and Recall"},
        {"Metric": "ROC-AUC Score", "Value": roc_auc, "Description": "Discriminative ability across all possible thresholds"},
        {"Metric": "PR-AUC (Average Precision)", "Value": pr_auc, "Description": "Precision-Recall trade-off area (vital for imbalanced data)"},
        {"Metric": "Matthews Correlation Coef (MCC)", "Value": mcc, "Description": "Balanced metric for imbalanced classes (-1 to +1)"},
        {"Metric": "Cohen's Kappa", "Value": kappa, "Description": "Inter-rater reliability adjusted for chance agreement"}
    ])
    metrics_df.to_csv(os.path.join(report_dir, "metrics_summary.csv"), index=False)

    # 6. Generate Matrix Representations
    print("[5/8] Generating matrix representations...")

    # (A) Confusion Matrix (Count and Normalized Heatmaps)
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=axes[0],
                annot_kws={"size": 14, "weight": "bold"},
                xticklabels=['Legitimate (0)', 'Fraud (1)'],
                yticklabels=['Legitimate (0)', 'Fraud (1)'])
    axes[0].set_title("Confusion Matrix (Raw Counts)\nTN: {tn:,} | FP: {fp:,} | FN: {fn:,} | TP: {tp:,}".format(
        tn=tn, fp=fp, fn=fn, tp=tp), fontsize=13, weight='bold', pad=12)
    axes[0].set_xlabel("Predicted Label", fontsize=11, weight='bold')
    axes[0].set_ylabel("Actual Label", fontsize=11, weight='bold')

    sns.heatmap(cm_norm, annot=True, fmt='.2%', cmap='Greens', cbar=False, ax=axes[1],
                annot_kws={"size": 14, "weight": "bold"},
                xticklabels=['Legitimate (0)', 'Fraud (1)'],
                yticklabels=['Legitimate (0)', 'Fraud (1)'])
    axes[1].set_title("Normalized Confusion Matrix (Recall per Class)\nSensitivity: {:.1%} | Specificity: {:.1%}".format(
        recall_1, specificity), fontsize=13, weight='bold', pad=12)
    axes[1].set_xlabel("Predicted Label", fontsize=11, weight='bold')
    axes[1].set_ylabel("Actual Label", fontsize=11, weight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, "confusion_matrix.png"), dpi=300)
    plt.close()

    # Save raw confusion matrix CSV
    pd.DataFrame({
        "Actual_Legitimate": [tn, fp],
        "Actual_Fraud": [fn, tp]
    }, index=["Predicted_Legitimate", "Predicted_Fraud"]).to_csv(os.path.join(report_dir, "confusion_matrix.csv"))

    # (B) Financial Cost & Risk Exposure Matrix
    # Estimated business costs:
    # - FP Cost: $150 (Cost of manual audit / investigation on false alarm)
    # - FN Cost: $35,000 (Average loss on an unblocked fraudulent loan)
    # - TP Benefit: $35,000 saved fraud loss
    cost_fp = 150
    cost_fn = 35000
    total_fp_cost = fp * cost_fp
    total_fn_cost = fn * cost_fn
    total_exposure = total_fp_cost + total_fn_cost
    unmitigated_loss = (tp + fn) * cost_fn
    net_fraud_savings = (tp * cost_fn) - total_fp_cost

    fig, ax = plt.subplots(figsize=(9, 6))
    cost_data = np.array([
        [0, total_fp_cost],
        [total_fn_cost, -net_fraud_savings]
    ])
    labels = np.array([
        [f"Clean Approvals\n$0 Friction\n({tn:,} apps)", f"Manual Audit Friction\n${total_fp_cost:,.0f} Cost\n({fp:,} false flags @ ${cost_fp})"],
        [f"Undetected Fraud Loss\n${total_fn_cost:,.0f} Exposure\n({fn:,} missed loans @ ${cost_fn:,})", f"Fraud Prevented\n${tp * cost_fn:,.0f} Saved\n({tp:,} caught fraud cases)"]
    ])
    sns.heatmap(cost_data, annot=labels, fmt="", cmap="YlOrRd", cbar=False, ax=ax,
                annot_kws={"size": 11, "weight": "bold"},
                xticklabels=["Action: Approved", "Action: Flagged for Review"],
                yticklabels=["Actual: Legitimate", "Actual: Fraudulent"])
    ax.set_title(f"Financial Impact & Exposure Matrix\nTotal Fraud Prevented: ${tp * cost_fn:,.0f} | Net Savings: ${net_fraud_savings:,.0f}",
                 fontsize=13, weight='bold', pad=14)
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, "financial_cost_matrix.png"), dpi=300)
    plt.close()

    # (C) Correlation Matrix Heatmap
    corr = data.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".3f", cmap="vlag", center=0, vmin=-1, vmax=1,
                linewidths=0.5, annot_kws={"size": 11, "weight": "bold"}, ax=ax)
    ax.set_title("Feature & Fraud Label Correlation Matrix", fontsize=13, weight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, "correlation_matrix.png"), dpi=300)
    plt.close()

    # 7. Generate Diagnostic Performance Graphs
    print("[6/8] Generating diagnostic curves (ROC, Precision-Recall, Thresholds)...")

    # (A) ROC Curve
    fpr, tpr, roc_thresh = roc_curve(y_test, y_proba)
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(fpr, tpr, color="#1f77b4", lw=2.5, label=f"Logistic Regression (AUC = {roc_auc:.4f})")
    ax.plot([0, 1], [0, 1], color="#999999", lw=1.5, linestyle="--", label="Random Classifier (AUC = 0.5000)")
    ax.scatter([fp / (tn + fp)], [recall_1], color="#d62728", s=80, zorder=5, label=f"Default Threshold 0.5 (TPR={recall_1:.2f}, FPR={fp/(tn+fp):.2f})")
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([-0.02, 1.05])
    ax.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=11, weight='bold')
    ax.set_ylabel("True Positive Rate (Recall / Sensitivity)", fontsize=11, weight='bold')
    ax.set_title("Receiver Operating Characteristic (ROC) Curve", fontsize=13, weight='bold', pad=12)
    ax.legend(loc="lower right", frameon=True, fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, "roc_curve.png"), dpi=300)
    plt.close()

    # (B) Precision-Recall Curve
    precision_curve, recall_curve, pr_thresh = precision_recall_curve(y_test, y_proba)
    baseline_pr = y_test.mean()
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(recall_curve, precision_curve, color="#2ca02c", lw=2.5, label=f"Logistic Regression (PR-AUC / AP = {pr_auc:.4f})")
    ax.axhline(y=baseline_pr, color="#999999", linestyle="--", lw=1.5, label=f"No-Skill Baseline (Prevalence = {baseline_pr:.2%})")
    ax.scatter([recall_1], [precision_1], color="#d62728", s=80, zorder=5, label=f"Default Threshold 0.5 (P={precision_1:.3f}, R={recall_1:.3f})")
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([-0.02, 1.05])
    ax.set_xlabel("Recall (Sensitivity)", fontsize=11, weight='bold')
    ax.set_ylabel("Precision (Positive Predictive Value)", fontsize=11, weight='bold')
    ax.set_title("Precision-Recall (PR) Curve for Imbalanced Fraud Detection", fontsize=13, weight='bold', pad=12)
    ax.legend(loc="upper right", frameon=True, fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, "precision_recall_curve.png"), dpi=300)
    plt.close()

    # (C) Precision, Recall & F1 vs Decision Threshold
    eval_thresholds = np.linspace(0.05, 0.95, 91)
    prec_list, rec_list, f1_list, acc_list = [], [], [], []
    for th in eval_thresholds:
        p_th = (y_proba >= th).astype(int)
        prec_list.append(precision_score(y_test, p_th, zero_division=0))
        rec_list.append(recall_score(y_test, p_th, zero_division=0))
        f1_list.append(f1_score(y_test, p_th, zero_division=0))
        acc_list.append(accuracy_score(y_test, p_th))

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(eval_thresholds, prec_list, color="#1f77b4", lw=2.2, label="Precision (Fraud)")
    ax.plot(eval_thresholds, rec_list, color="#ff7f0e", lw=2.2, label="Recall / Sensitivity")
    ax.plot(eval_thresholds, f1_list, color="#2ca02c", lw=2.2, label="F1-Score")
    ax.plot(eval_thresholds, acc_list, color="#7f7f7f", lw=1.8, linestyle=":", label="Overall Accuracy")
    ax.axvline(x=0.5, color="#d62728", linestyle="--", lw=1.2, label="Standard Threshold (0.50)")
    ax.set_xlabel("Decision Threshold", fontsize=11, weight='bold')
    ax.set_ylabel("Score (0.0 to 1.0)", fontsize=11, weight='bold')
    ax.set_title("Precision, Recall, F1 & Accuracy vs. Decision Threshold\nOperating Point Trade-Off Analysis", fontsize=13, weight='bold', pad=12)
    ax.legend(loc="center right", frameon=True, fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, "precision_recall_threshold_curve.png"), dpi=300)
    plt.close()

    # 8. Feature Importance, Probability Distribution & Calibration
    print("[7/8] Generating feature importance, calibration, and distribution plots...")

    # (A) Feature Importance (Coefficients)
    coef_df = pd.DataFrame({
        "Feature": feature_cols,
        "Coefficient": model.coef_[0]
    }).sort_values(by="Coefficient", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = ["#d62728" if c > 0 else "#1f77b4" for c in coef_df["Coefficient"]]
    ax.barh(coef_df["Feature"], coef_df["Coefficient"], color=colors, edgecolor="black", linewidth=0.6)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8)
    ax.set_xlabel("Logistic Regression Coefficient Weight", fontsize=11, weight='bold')
    ax.set_title("Model Feature Importance (Risk Drivers)\nPositive = Increases Fraud Risk | Negative = Reduces Fraud Risk", fontsize=12, weight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, "feature_importance.png"), dpi=300)
    plt.close()

    # (B) Probability Distribution Histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(y_proba[y_test == 0], bins=40, color="#1f77b4", label="Actual Legitimate (0)", stat="density", alpha=0.5, kde=True, ax=ax)
    sns.histplot(y_proba[y_test == 1], bins=40, color="#d62728", label="Actual Fraud (1)", stat="density", alpha=0.5, kde=True, ax=ax)
    ax.axvline(0.5, color="black", linestyle="--", lw=1.5, label="Decision Threshold (0.5)")
    ax.set_xlabel("Predicted Probability of Fraud", fontsize=11, weight='bold')
    ax.set_ylabel("Density", fontsize=11, weight='bold')
    ax.set_title("Predicted Fraud Probability Distribution by Actual Class", fontsize=13, weight='bold', pad=12)
    ax.legend(loc="upper right", frameon=True, fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, "prediction_probability_distribution.png"), dpi=300)
    plt.close()

    # (C) Summary Metrics Comparison Bar Chart
    fig, ax = plt.subplots(figsize=(10, 5))
    metrics_to_plot = {
        "Accuracy": accuracy,
        "Balanced\nAccuracy": balanced_acc,
        "Precision\n(Fraud)": precision_1,
        "Recall\n(Sensitivity)": recall_1,
        "Specificity": specificity,
        "F1-Score": f1_1,
        "ROC-AUC": roc_auc,
        "PR-AUC": pr_auc
    }
    bar_colors = ["#4e79a7", "#59a14f", "#e15759", "#f28e2b", "#76b7b2", "#edc948", "#b07aa1", "#ff9da7"]
    bars = ax.bar(list(metrics_to_plot.keys()), list(metrics_to_plot.values()), color=bar_colors, edgecolor="black", linewidth=0.6)
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.3f}",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, weight='bold')
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Score", fontsize=11, weight='bold')
    ax.set_title("Model Performance Scorecard\nAccuracy, Precision, Recall, and Discrimination Metrics", fontsize=13, weight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, "metrics_comparison_barchart.png"), dpi=300)
    plt.close()

    # (D) Calibration Curve
    prob_true, prob_pred = calibration_curve(y_test, y_proba, n_bins=10)
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.plot(prob_pred, prob_true, marker='o', lw=2, color="#4e79a7", label="Logistic Regression")
    ax.plot([0, 1], [0, 1], linestyle='--', color='#999999', label='Perfect Calibration')
    ax.set_xlabel("Mean Predicted Probability", fontsize=11, weight='bold')
    ax.set_ylabel("Fraction of Positives (Empirical Fraud)", fontsize=11, weight='bold')
    ax.set_title("Probability Calibration Curve (Reliability Diagram)", fontsize=13, weight='bold', pad=12)
    ax.legend(loc="upper left", frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, "calibration_curve.png"), dpi=300)
    plt.close()

    # 8. Write Markdown Performance Report
    print("[8/8] Writing executive Markdown report 'report/model_performance_report.md'...")
    md_content = f"""# 🛡️ Loan Fraud Detection - Model Evaluation & Performance Report

**Generated Date**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Model Architecture**: Logistic Regression (`class_weight='balanced'`, `max_iter=1000`)  
**Features Evaluated**: `{', '.join(feature_cols)}`  
**Target Label**: `{target_col}` (0 = Legitimate, 1 = Fraud)  

---

## 1. Executive Summary & Headline Scorecard

In financial fraud detection, **class imbalance is severe** (fraud represents **{metrics_summary['dataset_statistics']['fraud_prevalence_pct']}%** of all applications). Relying solely on raw **Accuracy** can be misleading, because a naive model that predicts every applicant is legitimate would achieve ~98% accuracy while capturing 0% of fraud.

For this reason, **Precision**, **Recall (Sensitivity)**, **PR-AUC**, and **Balanced Accuracy** serve as primary key performance indicators.

| Performance Metric | Score | Industry Interpretation |
| :--- | :---: | :--- |
| **Accuracy** | **{accuracy:.4f}** ({accuracy:.1%}) | Raw percentage of correct test decisions across both classes. |
| **Balanced Accuracy** | **{balanced_acc:.4f}** ({balanced_acc:.1%}) | Arithmetic mean of Sensitivity and Specificity; immune to class imbalance. |
| **Precision (Fraud Class)** | **{precision_1:.4f}** ({precision_1:.1%}) | Probability that an application flagged by the model is genuine fraud. |
| **Recall / Sensitivity** | **{recall_1:.4f}** ({recall_1:.1%}) | Percentage of all actual fraudsters successfully intercepted by the model. |
| **Specificity** | **{specificity:.4f}** ({specificity:.1%}) | Percentage of legitimate borrowers cleared without false accusations. |
| **F1-Score (Fraud)** | **{f1_1:.4f}** | Harmonic mean balancing fraud Precision and Recall. |
| **ROC-AUC Score** | **{roc_auc:.4f}** | Area under Receiver Operating Characteristic curve. |
| **PR-AUC (Average Precision)** | **{pr_auc:.4f}** | Area under Precision-Recall curve; key benchmark against baseline ({baseline_pr:.2%}). |
| **Matthews Correlation (MCC)** | **{mcc:.4f}** | Quality of binary classification considering all four confusion matrix quadrants. |
| **Cohen's Kappa** | **{kappa:.4f}** | Agreement between prediction and actual ground truth beyond random chance. |

---

## 2. Matrix Representations

### A. Confusion Matrix
The test partition contains **{len(y_test):,}** applications (**{(y_test == 0).sum():,}** legitimate and **{y_test.sum():,}** fraudulent).

| Category | Predicted Legitimate (0) | Predicted Fraud (1) | Total Actual |
| :--- | :---: | :---: | :---: |
| **Actual Legitimate (0)** | **{tn:,}** (TN - True Negatives) | **{fp:,}** (FP - False Alarms) | **{(y_test == 0).sum():,}** |
| **Actual Fraud (1)** | **{fn:,}** (FN - Missed Fraud) | **{tp:,}** (TP - Caught Fraud) | **{y_test.sum():,}** |
| **Total Predicted** | **{(tn + fn):,}** | **{(fp + tp):,}** | **{len(y_test):,}** |

![Confusion Matrix](confusion_matrix.png)

### B. Financial Impact & Risk Cost Matrix
Translating confusion matrix quadrants into dollar exposure:
- **True Positives ({tp:,} loans)**: Successfully intercepted fraud prevented estimated **${tp * cost_fn:,.0f}** in direct charge-off losses.
- **False Positives ({fp:,} loans)**: Legitimate borrowers flagged for secondary underwriting audit incurred **${total_fp_cost:,.0f}** in operational friction (@ ${cost_fp}/audit).
- **False Negatives ({fn:,} loans)**: Undetected fraud represents **${total_fn_cost:,.0f}** in capital loss exposure.
- **Net Fraud Mitigation Savings**: **${net_fraud_savings:,.0f}** saved versus zero model intervention.

![Financial Cost Matrix](financial_cost_matrix.png)

### C. Feature Correlation Matrix
Quantifying the linear relationship between applicant financial metrics and loan fraud:

![Correlation Matrix](correlation_matrix.png)

---

## 3. Diagnostic Curves & Threshold Trade-Off Analysis

### ROC Curve & Precision-Recall Curve
- **ROC Curve**: Tracks the True Positive Rate against the False Positive Rate across all cutoffs.
- **Precision-Recall Curve**: Evaluates precision retention as recall expands.

| ROC Curve | Precision-Recall Curve |
| :---: | :---: |
| ![ROC Curve](roc_curve.png) | ![Precision-Recall Curve](precision_recall_curve.png) |

### Decision Threshold Optimization
By adjusting the probability decision cutoff threshold, credit risk teams can calibrate the trade-off between **Precision** and **Recall**:

![Threshold Tuning Curve](precision_recall_threshold_curve.png)

| Threshold | Accuracy | Precision (Fraud) | Recall (Sensitivity) | F1-Score | True Positives | False Positives |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
"""
    for r in thresh_records:
        md_content += f"| **{r['threshold']:.2f}** | {r['accuracy']:.4f} | {r['precision']:.4f} | {r['recall']:.4f} | {r['f1_score']:.4f} | {r['true_positives']} | {r['false_positives']} |\n"

    md_content += f"""
---

## 4. Key Feature Drivers & Probability Distribution

### Model Feature Coefficients (Risk Drivers)
The Logistic Regression weights reveal which factors trigger higher fraud probabilities:

![Feature Importance](feature_importance.png)

- **Debt-to-Income Ratio (DTI)**: Coefficient `{model.coef_[0][3]:.6f}` — Higher DTI ratio strongly elevates loan vulnerability.
- **CIBIL / Credit Score**: Coefficient `{model.coef_[0][2]:.6f}` — Lower credit scores correlate with increased risk.
- **Monthly Income & Loan Amount**: Secondary volume and leverage indicators.

### Probability Distribution
Comparison of model risk scores assigned to genuine applicants versus fraudulent applicants:

![Probability Distribution](prediction_probability_distribution.png)

### Model Scorecard Summary
![Scorecard](metrics_comparison_barchart.png)

---

## 5. Artifacts Created in this Suite
All generated reports and high-resolution visuals are organized within this `report/` folder:
- 📊 [`confusion_matrix.png`](confusion_matrix.png)
- 💰 [`financial_cost_matrix.png`](financial_cost_matrix.png)
- 📈 [`roc_curve.png`](roc_curve.png)
- 🎯 [`precision_recall_curve.png`](precision_recall_curve.png)
- 🎚️ [`precision_recall_threshold_curve.png`](precision_recall_threshold_curve.png)
- 🔬 [`feature_importance.png`](feature_importance.png)
- 📉 [`prediction_probability_distribution.png`](prediction_probability_distribution.png)
- 🏆 [`metrics_comparison_barchart.png`](metrics_comparison_barchart.png)
- 📐 [`correlation_matrix.png`](correlation_matrix.png)
- 📏 [`calibration_curve.png`](calibration_curve.png)
- 📋 [`metrics_summary.json`](metrics_summary.json)
- 📑 [`metrics_summary.csv`](metrics_summary.csv)
- 📊 [`classification_report.csv`](classification_report.csv)
- 📄 [`classification_report.txt`](classification_report.txt)
- 🎛️ [`threshold_analysis.csv`](threshold_analysis.csv)
- 🔢 [`confusion_matrix.csv`](confusion_matrix.csv)
"""

    with open(os.path.join(report_dir, "model_performance_report.md"), "w", encoding="utf-8") as f:
        f.write(md_content)

    print("[SUCCESS] All reports, matrices, graphs, and metric files successfully generated in 'report/'!")

if __name__ == "__main__":
    generate_all_reports()
