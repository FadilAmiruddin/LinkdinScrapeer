import pandas as pd
import re
import json

# Function to remove duplicate links
def remove_duplicates(i, o):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(i)

    # Check if 'link' column exists in the DataFrame
    if 'link' not in df.columns:
        raise ValueError("The CSV file must contain a 'link' column.")

    # Remove duplicate links, keeping the first occurrence
    df_cleaned = df.drop_duplicates(subset='link', keep='first')

    # Save the cleaned DataFrame to a new CSV file
    df_cleaned.to_csv(o, index=False)
    print(f"Cleaned data saved to {o}")

def clean_description(description):
    try:
        # Convert the JSON string into a Python dictionary
        job_data = json.loads(description)
        
        # Extract the 'description' field
        raw_description = job_data.get('description', '')
        
        # Clean up the raw description to remove unwanted JSON structures
        cleaned_description = re.sub(r'^\{.*?"description":"(.*?)".*$', r'\1', raw_description)
        
        return cleaned_description
    except json.JSONDecodeError:
        return 'N/A'

# Function to parse the JSON in the 'Description' column
def parse_description(description):
    try:
        # Convert the JSON string into a Python dictionary
        job_data = json.loads(description)
        
        # Extract relevant fields
        job_info = {
            'title': job_data.get('title', 'N/A'),
            'company': job_data.get('hiringOrganization', {}).get('name', 'N/A'),
            'location': job_data.get('jobLocation', {}).get('address', {}).get('addressLocality', 'N/A'),
            'salary': job_data.get('baseSalary', {}).get('value', {}).get('minValue', 'N/A'),
            'max_salary': job_data.get('baseSalary', {}).get('value', {}).get('maxValue', 'N/A'),
        }
        return job_info
    except json.JSONDecodeError:
        return {
            'title': 'N/A',
            'company': 'N/A',
            'location': 'N/A',
            'salary': 'N/A',
            'max_salary': 'N/A'
        }

def processD(f):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(f)

    # Apply the function to each row in the DataFrame
    df['job_info'] = df['Description'].apply(parse_description)
    df['Description'] = df['Description'].apply(clean_description)

    # Drop rows where the 'Description' is 'N/A'
    df = df[df['Description'] != 'N/A']

    # Drop rows with duplicate descriptions
    df = df.drop_duplicates(subset='Description', keep='first')

    # Expand the 'job_info' column into separate columns
    job_info_df = pd.json_normalize(df['job_info'])

    # Concatenate the original DataFrame with the new job info DataFrame
    result_df = pd.concat([df, job_info_df], axis=1)

    # Save the result to a new CSV file
    result_df.to_csv('processed_job.csv', index=False)

    print(result_df.head())

# Remove duplicates
remove_duplicates("jobPost.csv", "output_cleaned.csv")

# Call the processing function
processD("output_cleaned.csv")
