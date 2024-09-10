import pandas as pd
import sys
import pyperclip

def csv_to_array_pandas(file_path):
    df = pd.read_csv(file_path)
    # Convert the DataFrame to a NumPy array
    csv_array = df.values
    return csv_array

# Example usage:
csv_file = 'processed_job.csv'
csv_array = csv_to_array_pandas(csv_file)

# Access the CSV data like an array
print(csv_array)  # Print entire CSV data
while True:
    r = input("enter row to copy desc of: ")
    pyperclip.copy(csv_array[int(r)][1])  # Print first row (first data row without headers)

