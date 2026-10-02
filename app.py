import streamlit as st
import pandas as pd
import joblib

# Set page config for a clean layout
st.set_page_config(page_title="Loan Fraud Risk Detector", page_icon="🛡️", layout="centered")

st.title("🛡️ Loan Fraud Detection & Risk Analysis")
st.write("Evaluate applicant loan requests for fraud indicators and view key risk drivers.")

# 1. Load model and features from model.pkl
saved_data = joblib.load("model.pkl")
if isinstance(saved_data, dict):
    model = saved_data["model"]
    feature_cols = saved_data.get("features", ["loan_amount_requested", "monthly_income", "cibil_score", "debt_to_income_ratio"])
else:
    model = saved_data
    feature_cols = ["loan_amount_requested", "monthly_income", "cibil_score", "debt_to_income_ratio"]

# 2. Input Fields
st.subheader("Applicant Financial Details")
col1, col2 = st.columns(2)

with col1:
    loan_amount = st.number_input(
        "Loan Amount Requested ($)",
        min_value=1000.0,
        max_value=2000000.0,
        value=350000.0,
        step=10000.0,
        help="Total principal loan amount applied for."
    )
    monthly_income = st.number_input(
        "Monthly Income ($)",
        min_value=500.0,
        max_value=500000.0,
        value=45000.0,
        step=2500.0,
        help="Verified monthly earnings of the primary applicant."
    )

with col2:
    credit_score = st.number_input(
        "Credit Score (CIBIL)",
        min_value=300.0,
        max_value=900.0,
        value=720.0,
        step=10.0,
        help="Credit score between 300 (poor) and 900 (excellent)."
    )
    dti_ratio = st.number_input(
        "Debt-to-Income Ratio (%)",
        min_value=0.0,
        max_value=100.0,
        value=22.0,
        step=1.0,
        help="Percentage of monthly income already committed to debt obligations."
    )

# 3. Single Predict Button
if st.button("Analyze Fraud Risk", type="primary"):
    input_df = pd.DataFrame([[loan_amount, monthly_income, credit_score, dti_ratio]], columns=feature_cols)

    # Base Logistic Regression prediction & probability
    base_prediction = model.predict(input_df)[0]
    base_proba = model.predict_proba(input_df)[0][1]

    # Rule-assisted financial risk factors evaluation
    risk_factors = []
    favorable_factors = []
    risk_points = 0

    # Factor 1: Debt-to-Income
    if dti_ratio >= 45.0:
        risk_factors.append(f"High Debt Burden: DTI is {dti_ratio:.1f}% (critical threshold is >40%).")
        risk_points += 35
    elif dti_ratio >= 35.0:
        risk_factors.append(f"Elevated Debt Burden: DTI is {dti_ratio:.1f}%.")
        risk_points += 15
    else:
        favorable_factors.append(f"Healthy Debt Ratio: DTI is {dti_ratio:.1f}%, leaving sufficient disposable income.")

    # Factor 2: Credit Score
    if credit_score < 580:
        risk_factors.append(f"Subprime Credit Profile: Score of {int(credit_score)} indicates high default and delinquency history.")
        risk_points += 40
    elif credit_score < 660:
        risk_factors.append(f"Fair Credit Profile: Score of {int(credit_score)} is below the prime lending benchmark.")
        risk_points += 20
    else:
        favorable_factors.append(f"Strong Credit Profile: Score of {int(credit_score)} demonstrates disciplined credit history.")

    # Factor 3: Loan to Annual Income Multiplier (Leverage)
    annual_income = monthly_income * 12.0
    leverage = (loan_amount / annual_income) if annual_income > 0 else 10.0
    if leverage > 4.0:
        risk_factors.append(f"Excessive Loan Leverage: Requested loan is {leverage:.1f}x annual income (standard limit is <3.5x).")
        risk_points += 30
    elif leverage > 3.0:
        risk_factors.append(f"Moderate Leverage: Requested loan is {leverage:.1f}x annual income.")
        risk_points += 10
    else:
        favorable_factors.append(f"Conservative Borrowing: Requested loan is {leverage:.1f}x annual income.")

    # Combined composite fraud & default risk percentage (0 - 100%)
    model_score = base_proba * 100.0
    final_risk_score = min(max(int((model_score * 0.4) + (risk_points * 0.6)), 5), 98)

    st.divider()

    # 4. Display Results & Risk Score
    col_score, col_verdict = st.columns([1, 2])
    with col_score:
        st.metric(
            label="Fraud Risk Score",
            value=f"{final_risk_score}%",
            delta="High Risk" if final_risk_score >= 50 else "Low Risk",
            delta_color="inverse"
        )
        st.progress(final_risk_score / 100.0)

    with col_verdict:
        if final_risk_score >= 60:
            st.error("### ⚠️ Flagged: High Fraud Risk")
            st.write("**Summary:** This application exhibits multiple high-risk indicators commonly associated with fraudulent applications and severe default risk.")
        elif final_risk_score >= 40:
            st.warning("### ⚠️ Caution: Moderate Risk")
            st.write("**Summary:** Application displays elevated leverage or debt patterns. Secondary manual underwriting verification is recommended.")
        else:
            st.success("### ✅ Clear: Legitimate Application")
            st.write("**Summary:** Application metrics align with typical verified borrowers with sound credit and manageable leverage.")

    # 5. Top Risk Factors & Positive Indicators Breakdown
    st.subheader("🔍 Decision Factors Breakdown")

    if risk_factors:
        st.markdown("**Top Risk Drivers:**")
        for factor in risk_factors:
            st.markdown(f"- ⚠️ {factor}")
    else:
        st.markdown("- *No adverse risk flags identified.*")

    if favorable_factors:
        st.markdown("**Favorable Profile Indicators:**")
        for factor in favorable_factors:
            st.markdown(f"- ✅ {factor}")
