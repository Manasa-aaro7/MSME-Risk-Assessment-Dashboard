import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title="MSME Risk Scoring", layout="wide")

# Store submitted data
if 'msme_data' not in st.session_state:
    st.session_state.msme_data = []

# Risk scoring function (placeholder logic)
def calculate_risk_score(inputs):
    score = 0
    score += (1 - inputs['EMI_to_Profit_Ratio']) * 10
    score += inputs['Profit_Loss_Ratio'] * 10
    score += inputs['Average_Monthly_Bank_Balance'] / 100000
    score += inputs['GST_Filing_Consistency'] * 10
    score += inputs['GST_Growth_Rate'] * 5
    score += inputs['Payroll_Consistency_Score'] * 10
    score -= inputs['Salary_Delay_Instances_Last_6_Months'] * 2
    score += inputs['Compliance_Payment_Consistency'] * 10
    score -= inputs['Loan_Default_History'] * 20
    score -= inputs['Days_Past_Due_on_Existing_Loans'] / 5
    score -= inputs['Num_Overdue_Loans'] * 2
    score -= inputs['Total_Overdue_Amount'] / 100000
    score += inputs['Previous_Loan_Approval_Rate'] * 10
    score -= inputs['Receivables_Aging_90plus_Percent'] * 5
    score += inputs['Employee_Count'] / 10

    if score >= 85:
        return "Low", score
    elif score >= 60:
        return "Medium", score
    else:
        return "High", score

# ---- UI ----
tab1, tab2 = st.tabs(["📋 MSME Risk Calculator", "📊 Admin Dashboard"])

with tab1:
    st.title("🧮 MSME Risk Scoring Calculator")

    with st.form("risk_form"):
        msme_name = st.text_input("MSME Name")

        def expander(label, explanation, source):
            with st.expander("ℹ️ Explanation"):
                st.markdown(f"**What it means**: {explanation}")
                st.markdown(f"**Source Document**: {source}")

        EMI_to_Profit_Ratio = st.number_input("EMI to Profit Ratio", 0.0, 10.0, 0.5)
        expander("EMI to Profit Ratio", "Total Monthly EMI ÷ Estimated Monthly Profit", "Loan statements + Profit & Loss")

        Profit_Loss_Ratio = st.number_input("Profit/Loss Ratio", -1.0, 2.0, 0.1)
        expander("Profit/Loss Ratio", "Net Profit ÷ Annual Revenue", "Profit & Loss Statement")

        Average_Monthly_Bank_Balance = st.number_input("Average Monthly Bank Balance (INR)", 0, 10_000_000, 100000)
        expander("Average Monthly Bank Balance", "Average of closing bank balance across last 6 months", "Bank statements")

        GST_Filing_Consistency = st.slider("GST Filing Consistency (0-1)", 0.0, 1.0, 1.0)
        expander("GST Filing Consistency", "Fraction of months GST was filed on time in last 6 months", "GST Portal/Returns")

        GST_Growth_Rate = st.number_input("GST Growth Rate (6 months, %)", min_value=-100.0, max_value=500.0, value=10.0, step=1.0)
        expander("GST Growth Rate", "Measures the percentage change in GST revenue between the most recent 3 months and the previous 3-month period. \nFormula:(GST in Recent 3 Months − GST in Previous 3 Months) / GST in Previous 3 Months × 100", "GST filings (GSTR-3B or GSTR-1)")

        Payroll_Consistency_Score = st.slider("Payroll Consistency Score (0-1)", 0.0, 1.0, 0.8)
        expander("Payroll Consistency Score", "Fraction of months salaries were paid on time (before 15th) in last 6 months", "Payroll software/sheets")

        Salary_Delay_Instances_Last_6_Months = st.number_input("Salary Delay Instances (Last 6 Months)", 0, 6, 0)
        expander("Salary Delay Instances", "Number of months in which salaries were paid post 15th", "Payroll reports")

        Compliance_Payment_Consistency = st.slider("Compliance Payment Consistency (0-1)", 0.0, 1.0, 1.0)
        expander("Compliance Payment Consistency", "Fraction of on-time PF/ESI/TDS/Professional Tax payments", "Compliance challans")

        Loan_Default_History = st.radio("Loan Default History", [0, 1])
        expander("Loan Default History", "1 if there were past loan defaults, 0 if never defaulted", "Credit Bureau Report")

        Days_Past_Due_on_Existing_Loans = st.number_input("Max Days Past Due on Existing Loans", 0, 365, 0)
        expander("Days Past Due", "Max no. of days an unpaid installment is overdue, among all current loans", "Loan statements/Credit Bureau")

        Num_Overdue_Loans = st.number_input("Number of Overdue Loans", 0, 10, 0)
        expander("Number of Overdue Loans", "Active loans with at least one missed payment", "Loan account summary")

        Total_Overdue_Amount = st.number_input("Total Overdue Amount (INR)", 0, 10_000_000, 0)
        expander("Total Overdue Amount", "Sum of overdue principal + interest, on all delinquent loans ", "Loan statements")

        Previous_Loan_Approval_Rate = st.slider("Previous Loan Approval Rate (0-1)", 0.0, 1.0, 1.0)
        expander("Previous Loan Approval Rate", "# of approved loans ÷ total loan applications", "Lender records")

        Receivables_Aging_90plus_Percent = st.slider("Receivables >90 Days (%)", 0.0, 100.0, 10.0)
        expander("Receivables Aging", "Percentage of receivables that are unpaid for >90 days", "Balance Sheet / Invoices")

        Employee_Count = st.number_input("Employee Count", 1, 1000, 10)
        expander("Employee Count", "Total number of salaried employees", "Payroll reports")

        uploaded_files = st.file_uploader("Upload Supporting Documents", accept_multiple_files=True)

        submitted = st.form_submit_button("Submit & Calculate Risk")

    if submitted:
        inputs = {
            'EMI_to_Profit_Ratio': EMI_to_Profit_Ratio,
            'Profit_Loss_Ratio': Profit_Loss_Ratio,
            'Average_Monthly_Bank_Balance': Average_Monthly_Bank_Balance,
            'GST_Filing_Consistency': GST_Filing_Consistency,
            'GST_Growth_Rate': GST_Growth_Rate,
            'Payroll_Consistency_Score': Payroll_Consistency_Score,
            'Salary_Delay_Instances_Last_6_Months': Salary_Delay_Instances_Last_6_Months,
            'Compliance_Payment_Consistency': Compliance_Payment_Consistency,
            'Loan_Default_History': Loan_Default_History,
            'Days_Past_Due_on_Existing_Loans': Days_Past_Due_on_Existing_Loans,
            'Num_Overdue_Loans': Num_Overdue_Loans,
            'Total_Overdue_Amount': Total_Overdue_Amount,
            'Previous_Loan_Approval_Rate': Previous_Loan_Approval_Rate,
            'Receivables_Aging_90plus_Percent': Receivables_Aging_90plus_Percent,
            'Employee_Count': Employee_Count,
        }

        risk_label, score = calculate_risk_score(inputs)

        st.success(f"**Risk Level: {risk_label}**  |  Score: {round(score, 2)}")

        progress = min(max(int(score), 0), 100)
        color = "green" if risk_label == "Low" else "orange" if risk_label == "Medium" else "red"
        st.markdown(f"""
            <div style="height: 25px; background-color: lightgray; border-radius: 5px;">
                <div style="height: 25px; width: {progress}%; background-color: {color}; text-align: center; color: white; border-radius: 5px;">
                    {risk_label}
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.session_state.msme_data.append({
            "MSME Name": msme_name,
            "Risk Level": risk_label,
            "Score": round(score, 2),
            "Inputs": inputs,
            "Files": uploaded_files
        })

with tab2:
    st.header("📊 Admin Dashboard: MSME Risk Overview")

    if st.session_state.msme_data:
        for i, entry in enumerate(st.session_state.msme_data):
            with st.expander(f"{entry['MSME Name']} - Risk: {entry['Risk Level']} (Score: {entry['Score']})"):
                st.json(entry["Inputs"])
                if entry["Files"]:
                    for file in entry["Files"]:
                        st.download_button(f"Download {file.name}", file.read(), file_name=file.name)
    else:
        st.info("No submissions yet.")
