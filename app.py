import streamlit as st

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Loan Approval Checker",
    page_icon="🏦",
    layout="centered"
)

# =========================
# Title
# =========================
st.title("🏦 Loan Approval Checker")
st.write("Fill in your details to check whether your loan will be approved or not.")

st.divider()

# =========================
# User Inputs
# =========================
st.subheader("📝 Enter Loan Details")

applicant_income = st.number_input(
    "Applicant Income",
    min_value=0,
    placeholder="Enter applicant income"
)

coapplicant_income = st.number_input(
    "Co-applicant Income",
    min_value=0,
    placeholder="Enter co-applicant income"
)

loan_amount = st.number_input(
    "Loan Amount",
    min_value=0,
    placeholder="Enter loan amount"
)

loan_term = st.number_input(
    "Loan Term (in months)",
    min_value=0,
    placeholder="e.g. 360"
)

credit_history = st.selectbox(
    "Credit History",
    options=[1, 0],
    format_func=lambda x: "Good (1)" if x == 1 else "Bad (0)"
)

# =========================
# Loan Decision Logic
# =========================
def loan_decision(app_income, co_income, loan_amt, term, credit):
    total_income = app_income + co_income

    # Simple approval rules
    if credit == 0:
        return "Rejected", "Poor credit history"

    if total_income < 5000:
        return "Rejected", "Income is too low"

    if loan_amt > total_income * 10:
        return "Rejected", "Loan amount too high compared to income"

    if term > 480:
        return "Rejected", "Loan term is too long"

    return "Approved", "Meets basic eligibility criteria"

# =========================
# Button Action
# =========================
st.divider()

if st.button("🔍 Check Loan Status", use_container_width=True):

    if applicant_income == 0 or loan_amount == 0 or loan_term == 0:
        st.warning("⚠️ Please fill all required fields.")
    else:
        status, reason = loan_decision(
            applicant_income,
            coapplicant_income,
            loan_amount,
            loan_term,
            credit_history
        )

        st.subheader("📄 Loan Decision")

        if status == "Approved":
            st.success("✅ **Loan Approved**")
            st.write(f"**Reason:** {reason}")
            st.balloons()
        else:
            st.error("❌ **Loan Rejected**")
            st.write(f"**Reason:** {reason}")

st.divider()
st.caption("⚠️ This is a rule-based demo system, not a real bank decision.")
