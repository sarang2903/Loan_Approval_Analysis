import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

st.set_page_config(page_title="Loan Prediction EDA + Chance", layout="wide")
st.title("🏦 Loan Prediction Dataset - EDA + Loan Approval Chance")

# =========================
# Load Dataset
# =========================
df = pd.read_csv("LP_Train.csv")

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

df["Dependents"] = df["Dependents"].replace("3+", "3").astype(int)

# Convert all object columns to string
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].astype(str)

st.success("✅ Data cleaned successfully")

# =========================
# Missing Values (SAFE)
# =========================
st.subheader("❓ Missing Values")
st.write(df.isnull().sum().to_dict())

# =========================
# Dataset Preview (SAFE)
# =========================
st.subheader("📌 Dataset Preview (First 20 Rows)")
st.write(df.head(20).to_dict())

# =========================
# Numerical Summary (SAFE)
# =========================
st.subheader("📊 Numerical Summary")
st.write(
    df[
        ["ApplicantIncome", "CoapplicantIncome", "LoanAmount",
         "Loan_Amount_Term", "Credit_History"]
    ].describe().round(2).to_dict()
)

# =========================
# Categorical Value Counts (SAFE)
# =========================
st.subheader("📌 Categorical Value Counts")
cat_cols = ["Gender", "Married", "Dependents", "Education", "Self_Employed"]

selected_cat = st.selectbox("Select column", cat_cols)
st.write(df[selected_cat].value_counts().to_dict())

# =========================
# Crosstab Plot (SAFE)
# =========================
st.subheader("📊 Loan Status vs Category")
selected_col = st.selectbox("Select column for Crosstab", cat_cols)

fig, ax = plt.subplots()
pd.crosstab(df[selected_col], df["Loan_Status"]).plot(kind="bar", ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)

# =========================
# Boxplot (SAFE)
# =========================
st.subheader("📦 ApplicantIncome vs Loan Status")
fig, ax = plt.subplots()
sb.boxplot(x="Loan_Status", y="ApplicantIncome", data=df, ax=ax)
st.pyplot(fig)

# =========================
# Barplot (SAFE)
# =========================
st.subheader("📊 CoapplicantIncome vs Loan Status")
fig, ax = plt.subplots()
sb.barplot(x="Loan_Status", y="CoapplicantIncome", data=df, ax=ax)
st.pyplot(fig)

# =========================
# Correlation (SAFE)
# =========================
st.subheader("📌 Correlation")
st.write(
    df[["ApplicantIncome", "CoapplicantIncome", "LoanAmount"]]
    .corr().round(2).to_dict()
)

# =========================
# Property Area vs Loan Status
# =========================
st.subheader("📌 Property Area vs Loan Status")
fig, ax = plt.subplots()
pd.crosstab(df["Property_Area"], df["Loan_Status"]).plot(kind="bar", ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)

# ==================================================
# 🎯 Loan Approval Chance (NO Arrow)
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
    score += 25 if total_income >= 10000 else 15 if total_income >= 5000 else 5
    score += 15 if loan_amount <= 150 else 10 if loan_amount <= 250 else 5
    score += 10 if loan_term <= 360 else 5
    return min(score, 100)

if st.button("Check Chance"):
    chance = loan_chance(income, co_income, loan_amount, loan_term, credit_history)
    st.success(f"✅ Loan Approval Chance: {chance}%")

    if chance >= 70:
        st.balloons()
        st.write("🎉 High chance of approval!")
    elif chance >= 40:
        st.warning("⚠️ Medium chance. Improve credit history.")
    else:
        st.error("❌ Low chance of approval.")
