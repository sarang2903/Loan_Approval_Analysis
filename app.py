import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Loan Prediction EDA + Approval Chance", layout="wide")

st.title("🏦 Loan Prediction Dataset - EDA + Loan Approval Chance")

# =========================
# Load Dataset
# =========================
df = pd.read_csv("../DataSets/LP_Train.csv")

st.subheader("📌 Raw Dataset")
st.dataframe(df)

# =========================
# Missing Values
# =========================
st.subheader("❓ Missing Values")
st.write(df.isnull().sum())

# =========================
# Data Cleaning
# =========================
df.Gender = df.Gender.fillna('Male')
df.Married = df.Married.fillna('Yes')
df.Dependents = df.Dependents.fillna(0)
df.Self_Employed = df.Self_Employed.fillna('No')
df.LoanAmount = df.LoanAmount.fillna(113.73)
df.Loan_Amount_Term = df.Loan_Amount_Term.fillna(344.53)
df.Credit_History = df.Credit_History.fillna(1.0)

df.Dependents = df.Dependents.replace('[+]', '', regex=True).astype('int64')

# =========================
# Sidebar Options
# =========================
st.sidebar.header("⚙️ Controls")
show_outliers_remove = st.sidebar.checkbox("Remove Outliers (ApplicantIncome)", value=False)

# =========================
# Outlier Removal
# =========================
if show_outliers_remove:
    i = "ApplicantIncome"
    q1 = np.percentile(df[i], 25)
    q3 = np.percentile(df[i], 75)
    iqr = q3 - q1
    c1 = q1 - 1.5 * iqr
    c2 = q3 + 1.5 * iqr

    w = df[(df[i] > c2) | (df[i] < c1)].index
    df = df.drop(labels=w, axis=0)

    st.success("✅ Outliers removed from ApplicantIncome!")

# =========================
# Describe
# =========================
st.subheader("📊 Numerical Summary")
st.write(df[['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History']].describe())

# =========================
# Categorical Value Counts
# =========================
st.subheader("📌 Categorical Columns Value Counts")
cat_cols = ['Gender','Married','Dependents','Education','Self_Employed','Property_Area']
selected_cat = st.selectbox("Select a categorical column", cat_cols)
st.write(df[selected_cat].value_counts())

# =========================
# Crosstab Bar Chart
# =========================
st.subheader("📌 Loan Status vs Category (Bar Chart)")
cols = ['Gender','Married','Dependents','Education','Self_Employed']
selected_col = st.selectbox("Select Column for Crosstab", cols)

fig, ax = plt.subplots()
pd.crosstab(df[selected_col], df['Loan_Status']).plot(kind='bar', ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)

# =========================
# Boxplot ApplicantIncome vs Loan_Status
# =========================
st.subheader("📌 ApplicantIncome vs Loan Status (Boxplot)")
fig, ax = plt.subplots()
sb.boxplot(x=df.Loan_Status, y=df.ApplicantIncome, ax=ax)
st.pyplot(fig)

# =========================
# Barplot CoapplicantIncome vs Loan_Status
# =========================
st.subheader("📌 CoapplicantIncome vs Loan Status (Barplot)")
fig, ax = plt.subplots()
sb.barplot(x=df.Loan_Status, y=df.CoapplicantIncome, ax=ax)
st.pyplot(fig)

# =========================
# Correlation
# =========================
st.subheader("📌 Correlation (Numeric Columns)")
st.write(df[['ApplicantIncome','CoapplicantIncome','LoanAmount']].corr(numeric_only=True))

# =========================
# Credit History vs Loan Status
# =========================
st.subheader("📌 Loan Status vs Credit History")
fig, ax = plt.subplots()
pd.crosstab(df['Loan_Status'], df['Credit_History']).plot(kind='bar', ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)

# =========================
# Loan Term vs Loan Status
# =========================
st.subheader("📌 Loan Amount Term vs Loan Status")
fig, ax = plt.subplots()
sb.barplot(x=df.Loan_Status, y=df.Loan_Amount_Term, ax=ax)
st.pyplot(fig)

# =========================
# Property Area vs Loan Status
# =========================
st.subheader("📌 Property Area vs Loan Status")
fig, ax = plt.subplots()
pd.crosstab(df['Property_Area'], df['Loan_Status']).plot(kind='bar', ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)

# =====================================================
# 🎯 Interactive Loan Approval Chance (User Input)
# =====================================================
st.title("🎯 Check Your Loan Approval Chance")

st.info("This is a **rule-based prediction** (not ML). If you want ML model prediction, tell me I will add it.")

name = st.text_input("Enter Your Name")
income = st.number_input("Applicant Income", min_value=0, value=5000)
co_income = st.number_input("Coapplicant Income", min_value=0, value=0)
loan_amount = st.number_input("Loan Amount", min_value=0, value=150)
loan_term = st.number_input("Loan Amount Term (Months)", min_value=0, value=360)
credit_history = st.selectbox("Credit History", [1.0, 0.0])

married = st.selectbox("Married", ["Yes", "No"])
education = st.selectbox("Education", ["Graduate", "Not Graduate"])
self_employed = st.selectbox("Self Employed", ["No", "Yes"])
property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

# =========================
# Rule-Based Chance Score
# =========================
def loan_chance(income, co_income, loan_amount, loan_term, credit_history,
                married, education, self_employed, property_area):

    score = 0

    # Credit history is most important
    if credit_history == 1.0:
        score += 50
    else:
        score += 10

    # Income
    total_income = income + co_income
    if total_income >= 10000:
        score += 20
    elif total_income >= 5000:
        score += 15
    else:
        score += 5

    # Loan amount (smaller = easier)
    if loan_amount <= 150:
        score += 15
    elif loan_amount <= 250:
        score += 10
    else:
        score += 5

    # Loan term
    if loan_term <= 360:
        score += 10
    else:
        score += 5

    # Education
    if education == "Graduate":
        score += 5

    # Self employed (slightly risky)
    if self_employed == "No":
        score += 5

    # Property Area
    if property_area == "Semiurban":
        score += 5
    elif property_area == "Urban":
        score += 3
    else:
        score += 2

    # Married (small positive)
    if married == "Yes":
        score += 2

    if score > 100:
        score = 100

    return score

if st.button("Check Approval Chance"):
    chance = loan_chance(income, co_income, loan_amount, loan_term, credit_history,
                         married, education, self_employed, property_area)

    st.subheader(f"👤 Applicant: {name if name else 'User'}")
    st.success(f"✅ Loan Approval Chance: **{chance}%**")

    if chance >= 70:
        st.balloons()
        st.write("🎉 **High chance of approval!**")
    elif chance >= 40:
        st.warning("⚠️ **Medium chance** (Improve credit history / reduce loan amount)")
    else:
        st.error("❌ **Low chance of approval** (Credit history and income are key)")
