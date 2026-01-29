import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Loan Approval Analysis", layout="wide")

st.title("🏦 Loan Approval Analysis & Prediction App")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("LP_Train.csv")
    
    df['Gender'].fillna('Male', inplace=True)
    df['Married'].fillna('Yes', inplace=True)
    df['Dependents'].fillna(0, inplace=True)
    df['Self_Employed'].fillna('No', inplace=True)
    df['LoanAmount'].fillna(128.0, inplace=True)
    df['Loan_Amount_Term'].fillna(360.0, inplace=True)
    df['Credit_History'].fillna(1.0, inplace=True)
    
    df['Dependents'] = df['Dependents'].replace('[+]', '', regex=True).astype(int)
    
    return df

df = load_data()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("📊 Navigation")
option = st.sidebar.radio(
    "Select Section",
    ["Dataset Overview", "EDA Visualizations", "Loan Approval Predictor"]
)

# -----------------------------
# DATASET OVERVIEW
# -----------------------------
if option == "Dataset Overview":
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    st.subheader("📌 Data Summary")
    st.write(df.describe())

    st.subheader("🧾 Missing Values")
    st.write(df.isnull().sum())

# -----------------------------
# EDA VISUALIZATIONS
# -----------------------------
elif option == "EDA Visualizations":
    st.subheader("📈 Exploratory Data Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Loan Status vs Credit History")
        fig, ax = plt.subplots()
        pd.crosstab(df['Loan_Status'], df['Credit_History']).plot(kind='bar', ax=ax)
        plt.xticks(rotation=0)
        st.pyplot(fig)

    with col2:
        st.write("Loan Status vs Applicant Income")
        fig, ax = plt.subplots()
        sb.boxplot(x=df['Loan_Status'], y=df['ApplicantIncome'], ax=ax)
        st.pyplot(fig)

    st.write("Property Area vs Loan Status")
    fig, ax = plt.subplots()
    pd.crosstab(df['Property_Area'], df['Loan_Status']).plot(kind='bar', ax=ax)
    plt.xticks(rotation=0)
    st.pyplot(fig)

# -----------------------------
# LOAN APPROVAL PREDICTOR
# -----------------------------
elif option == "Loan Approval Predictor":
    st.subheader("🧮 Check Your Loan Approval Chances")

    name = st.text_input("Applicant Name")
    income = st.number_input("Applicant Income", min_value=0)
    co_income = st.number_input("Coapplicant Income", min_value=0)
    loan_amt = st.number_input("Loan Amount", min_value=0)
    credit = st.selectbox("Credit History", [1.0, 0.0])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    married = st.selectbox("Married", ["Yes", "No"])

    if st.button("Check Approval Chance"):
        score = 0

        # Simple scoring logic
        if credit == 1.0:
            score += 50
        if income > 5000:
            score += 20
        if co_income > 2000:
            score += 10
        if loan_amt < 200:
            score += 10
        if education == "Graduate":
            score += 5
        if married == "Yes":
            score += 5

        if score >= 70:
            st.success(f"✅ {name}, High Chance of Loan Approval! ({score}%)")
        elif score >= 50:
            st.warning(f"⚠️ {name}, Moderate Chance of Loan Approval ({score}%)")
        else:
            st.error(f"❌ {name}, Low Chance of Loan Approval ({score}%)")

        st.info("📌 This is a rule-based estimation for educational purposes.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("👨‍💻 Developed for Academic Data Analysis & Streamlit Practice")
