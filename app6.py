# Data Pre Processing application using streamlit
import streamlit as st
import pandas as pd
import os
import numpy as np

# 1 Data Import
# 2 Treat the data (missing values, outliers, normalization)
# 3 Data export

# Enter the path here where all the temporary files will be stored
# For windows, use '\\' instead of '/'
# For linux or macOS, use '/'

tempfile = "\ temp.csv"
path = os.getcwd()
path = path+tempfile


# Title
st.title("Data Pre Processing")
st.markdown("This app is built by Sowjanya")


# Function to upload a csv file
def upload_file_csv():
    uploaded_file = st.sidebar.file_uploader("Upload a csv file", type="csv")
    if uploaded_file is not None:
        if st.sidebar.button("Upload csv file"):
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)
            df.to_csv(path)
        return


# Function to upload a excel file
def upload_file_excel():
    uploaded_file = st.sidebar.file_uploader("Upload a excel file", type="xlsx")
    if uploaded_file is not None:
        if st.sidebar.button("Upload excel file"):
            df = pd.read_excel(uploaded_file)
            st.dataframe(df)
            df.to_csv(path)
            return


# Data import
def data_import():
    st.sidebar.title("Data Import")
    file_options = ["csv", "xlsx"]
    file_type = st.sidebar.radio("Select file type", file_options)
    if file_type == "csv":
        upload_file_csv()
    elif file_type == "xlsx":
        upload_file_excel()

    return


# Data Treatment
def data_treatment_options():
    st.sidebar.title("Data Treatment")
    treatment_options = ["Missing Values", "Outliers", "Normalization"]
    treatment_type = st.sidebar.radio("Select treatment type", treatment_options)
    return treatment_type


# Function to give options for outlier treatment
def outliers_options():
    st.sidebar.title("Outliers Treatment")
    outliers_options_list = ["None", "IQR"]
    outliers_type = st.sidebar.radio("Select outliers option", outliers_options_list)
    if outliers_type == "IQR":
        st.sidebar.warning("Only numeric columns will be treated")
        df = pd.read_csv(path)
        column_name = st.sidebar.selectbox("Select column name", df.columns)
        if st.sidebar.button("Treat outliers"):
            outliers_iqr(column_name)


# Function to treat outliers using IQR method
def outliers_iqr(column_name):
    if column_name:
        df = pd.read_csv(path)
        q1 = df[column_name].quantile(0.25)
        q3 = df[column_name].quantile(0.75)
        IQR = q3 - q1
        lower_limit = q1 - 1.5 * IQR
        upper_limit = q3 + 1.5 * IQR
        removed_outlier = df[(df[column_name] > lower_limit) & (df[column_name] < upper_limit)]
        st.dataframe(removed_outlier)
        removed_outlier.to_csv(path)
        return removed_outlier


# Function to treat missing values using median
def treat_missing_values_median():
    df = pd.read_csv(path)
    df.fillna(df.median(), inplace=True)
    st.dataframe(df)
    df.to_csv(path, index=False)
    return


# Function to treat missing values using mode
def treat_missing_values_mode():
    df = pd.read_csv(path)
    df.fillna(df.mode(), inplace=True)
    st.dataframe(df)
    df.to_csv(path)
    return


# Missing Values options
def missing_values_options():
    st.sidebar.write("Choose a missing values option")
    missing_values_options_list = ["Median", "Mode"]
    missing_values_type = st.sidebar.radio("Select missing values option", missing_values_options_list)
    if missing_values_type == "Median":
        if st.sidebar.button("Process using median"):
            treat_missing_values_median()
    elif missing_values_type == "Mode":
        if st.sidebar.button("Process using mode"):
            treat_missing_values_mode()


# Function to normalize the data using standard scaler method
def normalize_data():
    df = pd.read_csv(path)
    X = df.select_dtypes(include=np.number)
    mean_X = np.mean(X)
    std_X = np.std(X)
    Xstd = (X - np.mean(X)) / np.std(X)
    st.dataframe(Xstd)
    Xstd.to_csv(path)

    return Xstd


# Normalization options
def normalization_options():
    st.sidebar.write("Choose a normalization option")
    normalization_options_list = ["None", "Standard Scaler"]
    normalization_type = st.sidebar.radio("Select normalization option", normalization_options_list)
    if normalization_type == "Standard Scaler":
        if st.sidebar.button("Process using Standard Scaler"):
            normalize_data()

#function to download the csv file
def download_csv():
    st.download_button(
        "Download csv file",
        file_name = "data.csv",
        data = path,
        mime = "text/csv"
    )

#function for Data export
def data_export():
    st.sidebar.title("Data export")
    if st.sidebar.button("Export data"):
        df = pd.read_csv(path)
        download_csv()



# main
def main():
    data_import()
    treatment_type = data_treatment_options()
    if treatment_type == "Missing Values":
        missing_values_options()
    elif treatment_type == "Outliers":
        outliers_options()
    elif treatment_type == "Normalization":
        normalization_options()
    data_export()

    return

main()