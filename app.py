
import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Loan Prediction EDA + Chance", layout="wide")

st.title("🏦 Loan Prediction Dataset - EDA + Loan Approval Chance")

# =========================
# Load Dataset
# =========================
df = pd.read_csv("LP_Train.csv")

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
df["Gender"] = df["Gender"].fillna("Male")
df["Married"] = df["Married"].fillna("Yes")
df["Dependents"] = df["Dependents"].fillna(0)
df["Self_Employed"] = df["Self_Employed"].fillna("No")
df["LoanAmount"] = df["LoanAmount"].fillna(113.73)
df["Loan_Amount_Term"] = df["Loan_Amount_Term"].fillna(344.53)
df["Credit_History"] = df["Credit_History"].fillna(1.0)

# Fix Dependents column like "3+"
df["Dependents"] = df["Dependents"].replace("[+]", "", regex=True).astype("int64")

st.success("✅ Data Cleaned Successfully!")

# =========================
# Sidebar
# =========================
st.sidebar.header("⚙️ Options")
remove_outliers = st.sidebar.checkbox("Remove Outliers (ApplicantIncome)", value=False)

# =========================
# Outlier Removal
# =========================
if remove_outliers:
    col = "ApplicantIncome"
    q1 = np.percentile(df[col], 25)
    q3 = np.percentile(df[col], 75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outlier_index = df[(df[col] < lower) | (df[col] > upper)].index
    df = df.drop(outlier_index)

    st.warning(f"⚠️ Removed {len(outlier_index)} outliers from ApplicantIncome")

# =========================
# Summary
# =========================
st.subheader("📊 Numerical Summary")
st.write(df[['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History']].describe())

# =========================
# Category Value Counts
# =========================
st.subheader("📌 Categorical Value Counts")
cat_cols = ['Gender','Married','Dependents','Education','Self_Employed','Property_Area']
selected_cat = st.selectbox("Select Categorical Column", cat_cols)
st.write(df[selected_cat].value_counts())

# =========================
# Crosstab Chart
# =========================
st.subheader("📊 Loan Status vs Category")
cols = ['Gender','Married','Dependents','Education','Self_Employed']
selected_col = st.selectbox("Select Column for Crosstab Plot", cols)

fig, ax = plt.subplots()
pd.crosstab(df[selected_col], df["Loan_Status"]).plot(kind="bar", ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)

# =========================
# Boxplot
# =========================
st.subheader("📦 ApplicantIncome vs Loan Status (Boxplot)")
fig, ax = plt.subplots()
sb.boxplot(x=df["Loan_Status"], y=df["ApplicantIncome"], ax=ax)
st.pyplot(fig)

# =========================
# Barplot
# =========================
st.subheader("📊 CoapplicantIncome vs Loan Status (Barplot)")
fig, ax = plt.subplots()
sb.barplot(x=df["Loan_Status"], y=df["CoapplicantIncome"], ax=ax)
st.pyplot(fig)

# =========================
# Correlation
# =========================
st.subheader("📌 Correlation")
st.write(df[['ApplicantIncome','CoapplicantIncome','LoanAmount']].corr(numeric_only=True))

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
# 🎯 Loan Approval Chance (User Input)
# ==================================================
st.title("🎯 Check Your Loan Approval Chance")

st.info("This is a simple rule-based chance score. For ML prediction, tell me I will add model.")

name = st.text_input("Enter Name")
income = st.number_input("Applicant Income", min_value=0, value=5000)
co_income = st.number_input("Coapplicant Income", min_value=0, value=0)
loan_amount = st.number_input("Loan Amount", min_value=0, value=150)
loan_term = st.number_input("Loan Term (Months)", min_value=0, value=360)
credit_history = st.selectbox("Credit History", [1.0, 0.0])

def loan_chance(income, co_income, loan_amount, loan_term, credit_history):
    score = 0

    # Credit History
    if credit_history == 1.0:
        score += 50
    else:
        score += 10

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
    if loan_term <= 360:
        score += 10
    else:
        score += 5

    if score > 100:
        score = 100

    return score

if st.button("Check Chance"):
    chance = loan_chance(income, co_income, loan_amount, loan_term, credit_history)

    st.subheader(f"👤 Applicant: {name if name else 'User'}")
    st.success(f"✅ Loan Approval Chance: **{chance}%**")

    if chance >= 70:
        st.balloons()
        st.write("🎉 High chance of approval!")
    elif chance >= 40:
        st.warning("⚠️ Medium chance. Try improving credit history / reduce loan amount.")
    else:
        st.error("❌ Low chance of approval. Credit history is very important.")


