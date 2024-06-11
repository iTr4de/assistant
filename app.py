import streamlit as st
import pandas as pd

# Load the dataset into a Pandas DataFrame
def load_dataset(file):
    try:
        data = pd.read_csv(file)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

    # Check for missing values and invalid date formats
    if data.isnull().values.any():
        warn("The dataset contains missing values")
    if not pd.to_datetime(data['date_column'], 
errors='coerce').notnull().all():
        warn("The dataset contains invalid date formats")

    # Compute some basic statistics about the dataset
    num_rows = len(data)
    num_cols = len(data.columns)
    data_types = data.dtypes
    memory_usage = data.memory_usage()
    unique_values = data.nunique()

    return {
        'num_rows': num_rows,
        'num_cols': num_cols,
        'data_types': data_types,
        'memory_usage': memory_usage,
        'unique_values': unique_values
    }

# Show the dataset summary in a Streamlit app
if __name__ == '__main__':
    file = st.file_uploader("Upload your CSV file")
    if file is not None:
        dataset = load_dataset(file)
        if dataset is not None:
            st.write("Dataset Summary:")
            st.write(f"Number of rows: {dataset['num_rows']}")
            st.write(f"Number of columns: {dataset['num_cols']}")
            st.write("Data types:")
            st.write(dataset['data_types'])
            st.write("Memory usage:")
            st.write(dataset['memory_usage'])
            st.write("Unique values per column:")
            st.write(dataset['unique_values'])
