import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np

# =========================
# IMPORTANT: Disable Arrow (fixes LargeUtf8 error)
# =========================
st.set_option("global.useArrow", False)

st.set_page_config(
    page_title="Loan Prediction EDA + Chance",
    layout="wide"
)

st.title("🏦 Loan Prediction Dataset - EDA + Loan Approval Chance")

# =========================
# Load Dataset
# =========================
df = pd.read_csv("LP_Train.csv")

# =========================
# Missing Values
# =========================
st.subheader("❓ Missing Values")
st.write(df.isnull().sum())

# =========================
# Data Cleaning
# =========================
df["Gender"] = df["Gender"].fillna("Male")
df["Married"] = df["Married"].fillna("Yes")
df["Dependents"] = df["Dependents"].fillna("0")
df["Self_Employed"] = df["Self_Employed"].fillna("No")
df["LoanAmount"] = df["LoanAmount"].fillna(df["LoanAmount"].median())
df["Loan_Amount_Term"] = df["Loan_Amount_Term"].fillna(360)
df["Credit_History"] = df["Credit_History"].fillna(1.0)

# Fix "3+" issue
df["Dependents"] = df["Dependents"].replace("3+", "3")
df["Dependents"] = df["Dependents"].astype(int)

# Convert ALL object columns to string (Arrow safety)
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].astype(str)

st.success("✅ Data cleaned successfully!")

# =========================
# Dataset Preview (SAFE)
# =========================
st.subheader("📌 Cleaned Dataset Preview")
st.table(df.head(50))

# =========================
# Sidebar
# =========================
st.sidebar.header("⚙️ Options")
remove_outliers = st.sidebar.checkbox("Remove Outliers (ApplicantIncome)")

# =========================
# Outlier Removal
# =========================
if remove_outliers:
    q1 = df["ApplicantIncome"].quantile(0.25)
    q3 = df["ApplicantIncome"].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    before = len(df)
    df = df[(df["ApplicantIncome"] >= lower) & (df["ApplicantIncome"] <= upper)]
    after = len(df)

    st.warning(f"⚠️ Removed {before - after} outliers")

# =========================
# Numerical Summary
# =========================
st.subheader("📊 Numerical Summary")
st.write(
    df[[
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount",
        "Loan_Amount_Term",
        "Credit_History"
    ]].describe()
)

# =========================
# Categorical Value Counts
# =========================
st.subheader("📌 Categorical Value Counts")
cat_cols = [
    "Gender", "Married", "Dependents",
    "Education", "Self_Employed", "Property_Area"
]

selected_cat = st.selectbox("Select column", cat_cols)
st.write(df[selected_cat].value_counts())

# =========================
# Crosstab Plot
# =========================
st.subheader("📊 Loan Status vs Category")
selected_col = st.selectbox("Select column for Crosstab", cat_cols[:-1])

fig, ax = plt.subplots()
pd.crosstab(df[selected_col], df["Loan_Status"]).plot(kind="bar", ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)

# =========================
# Boxplot
# =========================
st.subheader("📦 ApplicantIncome vs Loan Status")
fig, ax = plt.subplots()
sb.boxplot(x="Loan_Status", y="ApplicantIncome", data=df, ax=ax)
st.pyplot(fig)

# =========================
# Barplot
# =========================
st.subheader("📊 CoapplicantIncome vs Loan Status")
fig, ax = plt.subplots()
sb.barplot(x="Loan_Status", y="CoapplicantIncome", data=df, ax=ax)
st.pyplot(fig)

# =========================
# Correlation
# =========================
st.subheader("📌 Correlation")
st.write(
    df[[
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount"
    ]].corr()
)

# =========================
# Credit History vs Loan Status
# =========================
st.subheader("📌 Loan Status vs Credit History")
fig, ax = plt.subplots()
pd.crosstab(df["Loan_Status"], df["Credit_History"]).plot(kind="bar", ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)

# =========================
# Property Area vs Loan Status
# =========================
st.subheader("📌 Property Area vs Loan Status")
fig, ax = plt.subplots()
pd.crosstab(df["Property_Area"], df["Loan_Status"]).plot(kind="bar", ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)

# ==================================================
# 🎯 Loan Approval Chance
# ==================================================
st.title("🎯 Check Your Loan Approval Chance")

name = st.text_input("Enter Name")
income = st.number_input("Applicant Income", min_value=0, value=5000)
co_income = st.number_input("Coapplicant Income", min_value=0, value=0)
loan_amount = st.number_input("Loan Amount", min_value=0, value=150)
loan_term = st.number_input("Loan Term (Months)", min_value=0, value=360)
credit_history = st.selectbox("Credit History", [1.0, 0.0])

def loan_chance(income, co_income, loan_amount, loan_term, credit_history):
    score = 0

    score += 50 if credit_history == 1.0 else 10

    total_income = income + co_income
    if total_income >= 10000:
        score += 25
    elif total_income >= 5000:
        score += 15
    else:
        score += 5

    if loan_amount <= 150:
        score += 15
    elif loan_amount <= 250:
        score += 10
    else:
        score += 5

    score += 10 if loan_term <= 360 else 5

    return min(score, 100)

if st.button("Check Chance"):
    chance = loan_chance(
        income, co_income,
        loan_amount, loan_term,
        credit_history
    )

    st.subheader(f"👤 Applicant: {name if name else 'User'}")
    st.success(f"✅ Loan Approval Chance: {chance}%")

    if chance >= 70:
        st.balloons()
        st.write("🎉 High chance of approval!")
    elif chance >= 40:
        st.warning("⚠️ Medium chance. Improve credit history.")
    else:
        st.error("❌ Low chance of approval.")
