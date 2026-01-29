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
st.write("Upload dataset, explore EDA, and check loan eligibility using ML model.")

# ------------------ Upload Dataset ------------------
st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload LP_Train.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("⚠️ Please upload LP_Train.csv file from sidebar.")
    st.stop()

# ------------------ Show Dataset ------------------
st.subheader("📌 Raw Dataset")
st.dataframe(df)

# ------------------ Data Cleaning ------------------
st.subheader("🧹 Data Cleaning")

st.write("### Missing Values Before Filling")
st.write(df.isnull().sum())

df['Gender'] = df['Gender'].fillna('Male')
df['Married'] = df['Married'].fillna('Yes')
df['Dependents'] = df['Dependents'].fillna(0)
df['Self_Employed'] = df['Self_Employed'].fillna('No')
df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].mean())
df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mean())
df['Credit_History'] = df['Credit_History'].fillna(1.0)

df['Dependents'] = df['Dependents'].replace('[+]', '', regex=True).astype('int64')

st.success("✅ Missing values filled successfully!")

st.write("### Missing Values After Filling")
st.write(df.isnull().sum())

# ------------------ Sidebar Options ------------------
st.sidebar.header("📊 EDA Options")
eda_option = st.sidebar.selectbox(
    "Select EDA Chart",
    ["None", "Loan Status Count", "Categorical vs Loan Status", "Boxplot ApplicantIncome", "Credit History vs Loan Status", "Property Area vs Loan Status"]
)

# ------------------ EDA Charts ------------------
st.subheader("📊 Exploratory Data Analysis (EDA)")

if eda_option == "Loan Status Count":
    st.write("### Loan Status Count")
    fig, ax = plt.subplots()
    sb.countplot(x=df["Loan_Status"], ax=ax)
    st.pyplot(fig)

elif eda_option == "Categorical vs Loan Status":
    st.write("### Categorical Columns vs Loan Status")
    col = st.selectbox("Select Categorical Column", ['Gender','Married','Dependents','Education','Self_Employed'])
    fig, ax = plt.subplots()
    pd.crosstab(df[col], df['Loan_Status']).plot(kind='bar', ax=ax)
    plt.xticks(rotation=0)
    st.pyplot(fig)

elif eda_option == "Boxplot ApplicantIncome":
    st.write("### ApplicantIncome vs Loan Status")
    fig, ax = plt.subplots()
    sb.boxplot(x=df['Loan_Status'], y=df['ApplicantIncome'], ax=ax)
    st.pyplot(fig)

elif eda_option == "Credit History vs Loan Status":
    st.write("### Credit History vs Loan Status")
    fig, ax = plt.subplots()
    pd.crosstab(df['Loan_Status'], df['Credit_History']).plot(kind='bar', ax=ax)
    plt.xticks(rotation=0)
    st.pyplot(fig)

elif eda_option == "Property Area vs Loan Status":
    st.write("### Property Area vs Loan Status")
    fig, ax = plt.subplots()
    pd.crosstab(df['Property_Area'], df['Loan_Status']).plot(kind='bar', ax=ax)
    plt.xticks(rotation=0)
    st.pyplot(fig)

else:
    st.info("📌 Select any EDA chart from sidebar.")

# ------------------ ML Model Training ------------------
st.subheader("🤖 Train ML Model for Prediction")

df_model = df.copy()

# Encoding categorical columns
le = LabelEncoder()
for col in df_model.select_dtypes(include='object').columns:
    df_model[col] = le.fit_transform(df_model[col])

X = df_model.drop("Loan_Status", axis=1)
y = df_model["Loan_Status"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

st.success(f"✅ Model Trained Successfully! Accuracy: {acc*100:.2f}%")

# ------------------ User Input for Prediction ------------------
st.subheader("📝 Check Your Loan Eligibility (User Input)")

st.write("Fill details below and click **Predict Loan Status**")

col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Married", ["Yes", "No"])
    dependents = st.selectbox("Dependents", [0, 1, 2, 3])

with col2:
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

with col3:
    applicant_income = st.number_input("Applicant Income", min_value=0, value=5000)
    coapplicant_income = st.number_input("Coapplicant Income", min_value=0, value=0)
    loan_amount = st.number_input("Loan Amount", min_value=0, value=120)

loan_term = st.slider("Loan Amount Term", 12, 480, 360)
credit_history = st.selectbox("Credit History", [1.0, 0.0])

# Create input dataframe
user_data = pd.DataFrame({
    "Gender": [gender],
    "Married": [married],
    "Dependents": [dependents],
    "Education": [education],
    "Self_Employed": [self_employed],
    "ApplicantIncome": [applicant_income],
    "CoapplicantIncome": [coapplicant_income],
    "LoanAmount": [loan_amount],
    "Loan_Amount_Term": [loan_term],
    "Credit_History": [credit_history],
    "Property_Area": [property_area]
})

st.write("### Your Input Data")
st.dataframe(user_data)

# Encode user input
user_encoded = user_data.copy()
for col in user_encoded.select_dtypes(include='object').columns:
    user_encoded[col] = LabelEncoder().fit_transform(user_encoded[col])

# Prediction Button
if st.button("🔍 Predict Loan Status"):
    prediction = model.predict(user_encoded)[0]

    if prediction == 1:
        st.success("✅ Loan Approved (Y) 🎉")
    else:
        st.error("❌ Loan Not Approved (N)")
