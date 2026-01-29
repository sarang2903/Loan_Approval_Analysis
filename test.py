import streamlit as st
import pandas as pd

st.title("Dataset Checker")

st.write("App started successfully ✅")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    st.write("File uploaded ✅")
    df = pd.read_csv(file)
    st.dataframe(df.head())
else:
    st.warning("Please upload a CSV file")
