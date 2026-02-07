import streamlit as st
import pandas as pd

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Loan Approval Chance Checker",
    page_icon="🏦",
    layout="centered"
)

# =========================
# Title & Intro
# =========================
st.title("🏦 Loan Approval Chance Checker")
st.caption("Check your loan approval probability instantly 🚀")

st.markdown(
    """
    👋 **Welcome!**  
    Fill in your details below to estimate your loan approval chance.  
    This is a **rule-based score**, easy to understand and beginner-friendly.
    """
)

# =========================
# Sidebar (Optional Help)
# =========================
st.sidebar.header("ℹ️ How it works")
st.sidebar.write(
    """
    Your score is based on:
    - Credit History  
    - Total Income  
    - Loan Amount  
    - Loan Term  

    Higher score = better approval chance ✅
    """
)

# =========================
# User Input Section
# =========================
st.subheader("📝 Enter Your Details")

name = st.text_input("👤 Applicant Name", placeholder="e.g. Rahul")

income = st.slider(
    "💰 Applicant Income",
    min_value=0,
    max_value=50000,
    value=8000,
    step=500
)

co_income = st.slider(
    "💰 Co-applicant Income",
    min_value=0,
    max_value=30000,
    value=0,
    step=500
)

loan_amount = st.slider(
    "🏷️ Loan Amount (in thousands)",
    min_value=50,
    max_value=500,
    value=150,
    step=10
)

loan_term = st.selectbox(
    "📆 Loan Term (Months)",
    [120, 180, 240, 300, 360, 480]
)

credit_history = st.radio(
    "📄 Credit History",
    options=[1.0, 0.0],
    format_func=lambda x: "Good (No defaults)" if x == 1.0 else "Bad / No history"
)

# =========================
# Loan Chance Logic
# =========================
def loan_chance(income, co_income, loan_amount, loan_term, credit_history):
    score = 0

    # Credit History
    score += 50 if credit_history == 1.0 else 10

    # Income
    total_income = income + co_income
    if total_income >= 10000:
        score += 25
    elif total_income >= 5000:
        score += 15
    else:
        score += 5

    # Loan Amount
    if loan_amount <= 150:
        score += 15
    elif loan_amount <= 250:
        score += 10
    else:
        score += 5

    # Loan Term
    score += 10 if loan_term <= 360 else 5

    return min(score, 100)

# =========================
# Button Action
# =========================
st.divider()

if st.button("🔍 Check Loan Approval Chance", use_container_width=True):
    chance = loan_chance(income, co_income, loan_amount, loan_term, credit_history)

    st.subheader(f"👤 Applicant: {name if name else 'User'}")

    # Progress Bar
    st.progress(chance)

    st.markdown(f"### ✅ **Approval Chance: {chance}%**")

    # Result Messages
    if chance >= 70:
        st.success("🎉 Excellent! You have a **high chance** of loan approval.")
        st.balloons()
    elif chance >= 40:
        st.warning(
            "⚠️ Moderate chance.\n\n"
            "💡 Tip: Improve credit history or reduce loan amount."
        )
    else:
        st.error(
            "❌ Low chance of approval.\n\n"
            "📌 Credit history plays a major role."
        )

    # Friendly Summary
    with st.expander("📊 Why this score?"):
        st.write(
            f"""
            - **Total Income:** ₹{income + co_income}  
            - **Loan Amount:** ₹{loan_amount}k  
            - **Loan Term:** {loan_term} months  
            - **Credit History:** {"Good" if credit_history == 1.0 else "Poor"}  
            """
        )

st.divider()
st.caption("⚠️ This is a demo estimator. For real approval, banks use ML models & detailed checks.")
