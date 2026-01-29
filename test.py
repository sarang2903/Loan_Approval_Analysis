import streamlit as st
import pandas as pd

st.title("Dataset Checker App")

try:
    file = st.file_uploader("Upload your CSV file", type=["csv"])

    if file is not None:
        df = pd.read_csv(file)

        st.write("Preview:")
        st.dataframe(df.head())

        st.write("Shape:", df.shape)

        st.write("Missing Values:")
        st.write(df.isnull().sum())

        st.write("Data Types:")
        st.write(df.dtypes)

    else:
        st.info("Please upload a CSV file to check.")

except Exception as e:
    st.error("Error found ❌")
    st.write(e)
