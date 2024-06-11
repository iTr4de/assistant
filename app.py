import streamlit as st
import pandas as pd
import numpy as np

# Load the dataset into a Pandas DataFrame
def load_dataset(file, missing_value_option):
    try:
        data = pd.read_csv(file)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

    # Check if the DataFrame is empty
    if data.empty:
        st.warning("The uploaded dataset is empty.")
        return None

    # Calculate the percentage of missing values in each column
    missing_percentages = data.isnull().mean() * 100

    # Display the percentage of missing values for each column
    st.subheader("Missing Values Percentage")
    for column, percentage in missing_percentages.items():
        st.write(f"{column}: {percentage:.2f}%")

    # Check if the percentage of missing values is high (e.g., greater than 50%)
    if missing_percentages.max() > 50:
        st.warning("The dataset has a high percentage of missing values. Using mean imputation.")
        
        # Convert string columns to numeric if possible
        data = data.apply(pd.to_numeric, errors='coerce')
        
        # Fill missing values with mean
        data = data.fillna(data.mean())
    else:
        # Handle missing values based on user selection
        if missing_value_option == "Remove rows with missing values":
            data = data.dropna()
        elif missing_value_option == "Fill missing values with mean":
            # Convert string columns to numeric if possible
            data = data.apply(pd.to_numeric, errors='coerce')
            
            # Fill missing values with mean
            data = data.fillna(data.mean())
        elif missing_value_option == "Fill missing values with median":
            data = data.fillna(data.median())
        else:
            st.warning("Please select an option to handle missing values.")

    # Check if the dataset is empty after handling missing values
    if data.empty:
        st.error("The dataset is empty after handling missing values.")
        return None

    # Check for outliers
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
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
        missing_value_option = st.selectbox(
            "How do you want to handle missing values?",
            ("Keep missing values", "Remove rows with missing values", "Fill missing values with mean", "Fill missing values with median")
        )
        
        dataset = load_dataset(file, missing_value_option)
        
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
