import os
import subprocess

def create_streamlit_html(status_type):
    if status_type == "low":
        loan_amount = "350,000.00"
        credit_score = "760.00"
        monthly_income = "45,000.00"
        dti_ratio = "22.0 %"
        score_val = "12%"
        delta_label = "Low Risk"
        delta_class = "delta-low"
        progress_val = "12%"
        progress_color = "#10B981"
        callout_type = "callout-success"
        callout_title = "✅ Clear: Legitimate Application"
        callout_desc = "Application metrics align with typical verified borrowers with sound credit and manageable leverage ratios."
        drivers_title = "Favorable Profile Indicators:"
        drivers = [
            ("✅", "Healthy Debt Ratio:", "DTI is 22.0%, leaving sufficient disposable income.", "#047857"),
            ("✅", "Strong Credit Profile:", "Score of 760 demonstrates disciplined credit history.", "#047857"),
            ("✅", "Conservative Borrowing:", "Requested loan is 0.6x annual income.", "#047857")
        ]
    elif status_type == "high":
        loan_amount = "1,200,000.00"
        credit_score = "480.00"
        monthly_income = "15,000.00"
        dti_ratio = "65.0 %"
        score_val = "88%"
        delta_label = "High Risk"
        delta_class = "delta-high"
        progress_val = "88%"
        progress_color = "#EF4444"
        callout_type = "callout-error"
        callout_title = "⚠️ Flagged: High Fraud Risk"
        callout_desc = "This application exhibits multiple high-risk indicators commonly associated with fraudulent applications and severe default risk."
        drivers_title = "Top Risk Drivers:"
        drivers = [
            ("⚠️", "High Debt Burden:", "DTI is 65.0% (critical threshold is >40%).", "#B91C1C"),
            ("⚠️", "Subprime Credit Profile:", "Score of 480 indicates high default and delinquency history.", "#B91C1C"),
            ("⚠️", "Excessive Loan Leverage:", "Requested loan is 6.7x annual income (standard limit is <3.5x).", "#B91C1C")
        ]
    else: # moderate
        loan_amount = "650,000.00"
        credit_score = "630.00"
        monthly_income = "25,000.00"
        dti_ratio = "38.0 %"
        score_val = "48%"
        delta_label = "Moderate Risk"
        delta_class = "delta-mod"
        progress_val = "48%"
        progress_color = "#F59E0B"
        callout_type = "callout-warning"
        callout_title = "⚠️ Caution: Moderate Risk"
        callout_desc = "Application displays elevated leverage or debt patterns. Secondary manual underwriting verification is recommended."
        drivers_title = "Top Risk Drivers:"
        drivers = [
            ("⚠️", "Elevated Debt Burden:", "DTI is 38.0%.", "#B45309"),
            ("⚠️", "Fair Credit Profile:", "Score of 630 is below the prime lending benchmark.", "#B45309"),
            ("⚠️", "Moderate Leverage:", "Requested loan is 2.2x annual income.", "#B45309")
        ]

    drivers_html = ""
    for icon, bold_txt, norm_txt, color in drivers:
        drivers_html += f"""
        <li class="factor-item">
            <span class="factor-icon">{icon}</span>
            <span class="factor-bold" style="color: {color};">{bold_txt}</span>
            <span class="factor-text">{norm_txt}</span>
        </li>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        background: #FFFFFF;
        margin: 0;
        padding: 0;
    }}
    .browser-window {{
        width: 1000px;
        margin: 0 auto;
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        overflow: hidden;
    }}
    .window-header {{
        background: #F1F5F9;
        padding: 10px 16px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid #E2E8F0;
        gap: 12px;
    }}
    .window-buttons {{
        display: flex;
        gap: 7px;
    }}
    .win-btn {{
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }}
    .btn-red {{ background: #EF4444; }}
    .btn-yellow {{ background: #F59E0B; }}
    .btn-green {{ background: #10B981; }}
    .url-bar {{
        flex: 1;
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 5px 12px;
        font-size: 13px;
        color: #475569;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .app-content {{
        padding: 36px 48px;
        background: #FFFFFF;
    }}
    .app-title {{
        font-size: 26px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .app-subtitle {{
        font-size: 15px;
        color: #64748B;
        margin-bottom: 24px;
    }}
    .card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 22px 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .card-title {{
        font-size: 17px;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 18px;
    }}
    .grid-2 {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 18px 24px;
    }}
    .input-group label {{
        display: block;
        font-size: 13.5px;
        font-weight: 500;
        color: #334155;
        margin-bottom: 6px;
    }}
    .input-box {{
        display: flex;
        align-items: center;
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14.5px;
        color: #0F172A;
        font-weight: 500;
    }}
    .input-box .stepper {{
        margin-left: auto;
        display: flex;
        gap: 6px;
        color: #94A3B8;
        font-size: 12px;
    }}
    .btn-submit {{
        display: inline-block;
        background: #FF4B4B;
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        padding: 10px 22px;
        font-size: 14.5px;
        font-weight: 600;
        margin: 4px 0 20px 0;
        box-shadow: 0 1px 2px rgba(255, 75, 75, 0.2);
    }}
    .divider {{
        height: 1px;
        background: #E2E8F0;
        margin: 16px 0 24px 0;
    }}
    .results-row {{
        display: grid;
        grid-template-columns: 240px 1fr;
        gap: 20px;
        margin-bottom: 24px;
    }}
    .metric-box {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .metric-label {{
        font-size: 13px;
        font-weight: 500;
        color: #64748B;
        margin-bottom: 4px;
    }}
    .metric-value {{
        font-size: 32px;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
    }}
    .metric-delta {{
        display: inline-block;
        margin-top: 6px;
        font-size: 12px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
    }}
    .delta-low {{
        background: #ECFDF5;
        color: #059669;
    }}
    .delta-high {{
        background: #FEF2F2;
        color: #DC2626;
    }}
    .delta-mod {{
        background: #FFFBEB;
        color: #D97706;
    }}
    .progress-bar-wrap {{
        margin-top: 10px;
        height: 7px;
        background: #E2E8F0;
        border-radius: 4px;
        overflow: hidden;
    }}
    .progress-bar-fill {{
        height: 100%;
        width: {progress_val};
        background: {progress_color};
        border-radius: 4px;
    }}
    .callout-box {{
        border-radius: 8px;
        padding: 16px 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .callout-success {{
        background: #F0FDF4;
        border: 1.5px solid #86EFAC;
    }}
    .callout-error {{
        background: #FEF2F2;
        border: 1.5px solid #FCA5A5;
    }}
    .callout-warning {{
        background: #FFFBEB;
        border: 1.5px solid #FDE68A;
    }}
    .callout-title {{
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 6px;
    }}
    .callout-success .callout-title {{ color: #15803D; }}
    .callout-error .callout-title {{ color: #B91C1C; }}
    .callout-warning .callout-title {{ color: #B45309; }}
    .callout-body {{
        font-size: 13.5px;
        line-height: 1.5;
        color: #334155;
    }}
    .breakdown-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 20px 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .breakdown-title {{
        font-size: 17px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .breakdown-subtitle {{
        font-size: 14px;
        font-weight: 600;
        color: #475569;
        margin-bottom: 10px;
    }}
    .factor-list {{
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }}
    .factor-item {{
        display: flex;
        align-items: baseline;
        gap: 8px;
        font-size: 14px;
        line-height: 1.45;
    }}
    .factor-icon {{
        font-size: 13px;
    }}
    .factor-bold {{
        font-weight: 600;
    }}
    .factor-text {{
        color: #334155;
    }}
</style>
</head>
<body>
<div class="browser-window">
    <div class="window-header">
        <div class="window-buttons">
            <div class="win-btn btn-red"></div>
            <div class="win-btn btn-yellow"></div>
            <div class="win-btn btn-green"></div>
        </div>
        <div class="url-bar">
            <span>🔒</span>
            <span>http://localhost:8501</span>
            <span style="margin-left: auto; color: #94A3B8;">LoanGuard-AI · Streamlit</span>
        </div>
    </div>
    <div class="app-content">
        <div class="app-title">
            <span>🛡️</span>
            <span>LoanGuard-AI: Loan Fraud Detection & Risk Analysis</span>
        </div>
        <div class="app-subtitle">Evaluate applicant loan requests for fraud indicators and view key risk drivers.</div>

        <div class="card">
            <div class="card-title">Applicant Financial Details</div>
            <div class="grid-2">
                <div class="input-group">
                    <label>Loan Amount Requested ($)</label>
                    <div class="input-box">
                        <span>{loan_amount}</span>
                        <span class="stepper">− &nbsp; +</span>
                    </div>
                </div>
                <div class="input-group">
                    <label>Credit Score (CIBIL)</label>
                    <div class="input-box">
                        <span>{credit_score}</span>
                        <span class="stepper">− &nbsp; +</span>
                    </div>
                </div>
                <div class="input-group">
                    <label>Monthly Income ($)</label>
                    <div class="input-box">
                        <span>{monthly_income}</span>
                        <span class="stepper">− &nbsp; +</span>
                    </div>
                </div>
                <div class="input-group">
                    <label>Debt-to-Income Ratio (%)</label>
                    <div class="input-box">
                        <span>{dti_ratio}</span>
                        <span class="stepper">− &nbsp; +</span>
                    </div>
                </div>
            </div>
        </div>

        <div>
            <button class="btn-submit">Analyze Fraud Risk</button>
        </div>

        <div class="divider"></div>

        <div class="results-row">
            <div class="metric-box">
                <div class="metric-label">Fraud Risk Score</div>
                <div class="metric-value">{score_val}</div>
                <div class="metric-delta {delta_class}">Status: {delta_label}</div>
                <div class="progress-bar-wrap">
                    <div class="progress-bar-fill"></div>
                </div>
            </div>
            <div class="callout-box {callout_type}">
                <div class="callout-title">{callout_title}</div>
                <div class="callout-body"><b>Summary:</b> {callout_desc}</div>
            </div>
        </div>

        <div class="breakdown-card">
            <div class="breakdown-title">
                <span>🔍</span>
                <span>Decision Factors Breakdown</span>
            </div>
            <div class="breakdown-subtitle">{drivers_title}</div>
            <ul class="factor-list">
                {drivers_html}
            </ul>
        </div>
    </div>
</div>
</body>
</html>
"""
    return html

def render_images():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    assets_dir = os.path.abspath("report_assets")
    os.makedirs(assets_dir, exist_ok=True)

    configs = [
        ("low", os.path.join(assets_dir, "fig_8_2_app_low_risk.png")),
        ("high", os.path.join(assets_dir, "fig_8_3_app_high_risk.png")),
        ("moderate", os.path.join(assets_dir, "fig_8_4_app_moderate_risk.png")),
    ]

    for status_type, output_png in configs:
        html_content = create_streamlit_html(status_type)
        temp_html = os.path.abspath(f"temp_render_{status_type}.html")
        with open(temp_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        cmd = [
            chrome_path,
            "--headless=new",
            "--disable-gpu",
            "--force-device-scale-factor=2",
            "--window-size=1000,940",
            f"--screenshot={output_png}",
            f"file:///{temp_html.replace(os.sep, '/')}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(output_png):
            print(f"[SUCCESS] Rendered {os.path.basename(output_png)}")
        else:
            print(f"[ERROR] Failed {output_png}: {res.stderr}")

        if os.path.exists(temp_html):
            os.remove(temp_html)

if __name__ == "__main__":
    render_images()
