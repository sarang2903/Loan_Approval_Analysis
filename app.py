import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="Loan Prediction App", layout="wide")

st.title("🏦 Loan Prediction + EDA (Interactive Streamlit App)")

# ============================
# Load Dataset
# ============================
st.sidebar.header("📂 Dataset Options")

file = st.sidebar.file_uploader("Upload LP_Train.csv", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
else:
    df = pd.read_csv("LP_Train.csv")

st.subheader("📌 Raw Dataset")
st.dataframe(df)

# ============================
# Missing Values Handling (Your Logic)
# ============================
st.subheader("🧹 Data Cleaning")

st.write("### Missing Values Before")
st.write(df.isnull().sum())

df.Gender = df.Gender.fillna('Male')
df.Married = df.Married.fillna('Yes')
df.Dependents = df.Dependents.fillna(0)
df.Self_Employed = df.Self_Employed.fillna('No')
df.LoanAmount = df.LoanAmount.fillna(113.73)
df.Loan_Amount_Term = df.Loan_Amount_Term.fillna(344.53)
df.Credit_History = df.Credit_History.fillna(1.0)

df.Dependents = df.Dependents.replace('[+]', '', regex=True).astype('int64')

st.success("✅ Missing values handled!")

st.write("### Missing Values After")
st.write(df.isnull().sum())

# ============================
# Basic Stats
# ============================
st.subheader("📊 Numerical Columns Summary")
st.write(df[['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History']].describe())

# ============================
# Sidebar EDA Options
# ============================
st.sidebar.header("📊 EDA Charts")

chart = st.sidebar.selectbox(
    "Select Chart",
    [
        "None",
        "Loan Status Count",
        "Categorical vs Loan Status",
        "Boxplot: ApplicantIncome vs Loan_Status",
        "Barplot: CoapplicantIncome vs Loan_Status",
        "Credit History vs Loan Status",
        "Loan Term vs Loan Status",
        "Loan Term vs Credit History",
        "Property Area vs Loan Status"
    ]
)

st.subheader("📈 EDA Visualization")

if chart == "Loan Status Count":
    fig, ax = plt.subplots()
    sb.countplot(x=df["Loan_Status"], ax=ax)
    st.pyplot(fig)

elif chart == "Categorical vs Loan Status":
    cols = ['Gender','Married','Dependents','Education','Self_Employed']
    selected_col = st.selectbox("Select Column", cols)

    fig, ax = plt.subplots()
    pd.crosstab(df[selected_col], df['Loan_Status']).plot(kind='bar', ax=ax)
    plt.xticks(rotation=0)
    st.pyplot(fig)

elif chart == "Boxplot: ApplicantIncome vs Loan
