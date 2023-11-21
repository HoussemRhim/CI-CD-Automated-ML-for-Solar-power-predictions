import os
import pandas as pd
from google.cloud import storage

# Set the project ID
PROJECT_ID = "reflected-oath-405515"
# Set the path to your JSON credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./reflected-oath-405515-70b04b6190ad.json"

def load_energy_data_from_csv():
    """
    Helper function to load electricity data from disk

    Solar energy data found on kaggle:
    https://www.kaggle.com/datasets/fvcoppen/solarpanelspower/code?select=metingen_27feb2022.csv
    
    :return: loaded pandas df
    """

    # Load CSV file into a DataFrame
    df = pd.read_csv('data/PV_Elec_Gas2.csv')

    # Upload data to GCS bucket
    upload_to_gcs(df, 'data_bucket_raw', 'energy_data.csv')

    return df

def upload_to_gcs(data, bucket_name, file_name):
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    client = storage.Client(project=PROJECT_ID)
    bucket = client.get_bucket(bucket_name)

    # Convert DataFrame to CSV string
    csv_data = data.to_csv(index=False)

    # Upload CSV string to GCS
    blob = bucket.blob(file_name)
    blob.upload_from_string(csv_data, content_type='text/csv')