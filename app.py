import streamlit as st
import pandas as pd
import numpy as np

# Load the dataset into a Pandas DataFrame
def load_dataset(file):
    try:
        data = pd.read_csv(file)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

    # Check if the DataFrame is empty
    if data.empty:
        st.warning("The uploaded dataset is empty.")
        return None

    # Check for missing values and outliers
    if data.isnull().values.any():
        st.warning("The dataset contains missing values")
        data = data.dropna()
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - (iqr * 1.5)
    upper_bound = q3 + (iqr * 1.5)
    data = data[(data >= lower_bound) & (data <= upper_bound)]

    # Compute some basic statistics about the dataset
    num_rows = len(data)
    num_cols = len(data.columns)
    data_types = data.dtypes
    memory_usage = data.memory_usage()
    unique_values = data.nunique()

    return {
        'data': data,
        'num_rows': num_rows,
        'num_cols': num_cols,
        'data_types': data_types,
        'memory_usage': memory_usage,
        'unique_values': unique_values
    }

# Show the dataset summary in a Streamlit app
def main():
    st.title("Dataset Summary")
    file = st.file_uploader("Upload your CSV file", type=["csv"])
    if file is not None:
        dataset = load_dataset(file)
        if dataset is not None:
            st.subheader("Dataset Preview")
            st.write(dataset['data'].head())

            st.subheader("Dataset Summary")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Number of rows:", dataset['num_rows'])
                st.write("Number of columns:", dataset['num_cols'])
            with col2:
                st.write("Memory usage:")
                st.write(dataset['memory_usage'])

            st.subheader("Data Types")
            st.write(dataset['data_types'])

            st.subheader("Unique Values per Column")
            st.write(dataset['unique_values'])

if __name__ == '__main__':
    main()
