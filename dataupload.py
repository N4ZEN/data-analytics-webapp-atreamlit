import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#title
st.title('Customer Segmentation App')

#add sidebar
st.sidebar.subheader("Visualization Controls")

#setup file upload
uploaded_file =st.sidebar.file_uploader(label="Upload your CSV file", type=['csv','xlsx'])


global df
if uploaded_file is not None:
    print(uploaded_file)
    print("No file Uploaded.")

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        print(e)
        df = pd.read_excel(uploaded_file)
try:
    st.write(df)
except Exception as e:
    print(e)
    st.write("Please upload file to the application.")

