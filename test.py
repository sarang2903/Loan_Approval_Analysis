import streamlit as st
import pandas as pd

st.title("✅ Dataset Checker")

# Upload file
file = st.file_uploader("Upload CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    st.subheader("📌 Dataset Preview")
    st.dataframe(df.head())

    st.subheader("📌 Shape (Rows, Columns)")
    st.write(df.shape)

    st.subheader("📌 Missing Values")
    st.write(df.isnull().sum())

    st.subheader("📌 Column Data Types")
    st.write(df.dtypes)
