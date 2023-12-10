import os
import pandas as pd
from google.cloud import storage


# Set the project ID
PROJECT_ID = "reflected-oath-405515"
# Set the path to your JSON credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./terraform/reflected-oath-405515-70b04b6190ad.json"
"""
def load_weather_data():
    ###
    Helper function to load weather data

    Downloaded from publicly available weather data from https://meteostat.net/
    For the city of Antwerp (2011-Today)

    :return: loaded pandas df
    ###

    # Load each year file of data
    df_2017 = pd.read_csv('./data/weather_2017.csv')
    df_2018 = pd.read_csv('./data/weather_2018.csv')
    df_2019 = pd.read_csv('./data/weather_2019.csv')

    # Combine multiple years of weather data into one df
    weather_data_combined = pd.concat([df_2017, df_2018, df_2019], ignore_index=True)
    
    # Upload data to GCS bucket
    upload_to_gcs(weather_data_combined, 'data_bucket_raw', 'weather_data.csv')

    return weather_data_combined

def upload_to_gcs(data, bucket_name, file_name):
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    client = storage.Client(project=PROJECT_ID)
    bucket = client.get_bucket(bucket_name)

    # Convert DataFrame to CSV string
    csv_data = data.to_csv(index=False)

    # Upload CSV string to GCS
    blob = bucket.blob(file_name)
    blob.upload_from_string(csv_data, content_type='text/csv')
"""

def upload_to_gcp(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    # Create a client for interacting with Google Cloud Storage
    storage_client = storage.Client()

    # Reference an existing bucket.
    bucket = storage_client.bucket(bucket_name)

    # Create a blob and upload the file
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def load_weather_data(bucket_name, destination_blob_name):

    # Load each year file of data
    df_2017 = pd.read_csv('./data/weather_2017.csv')
    df_2018 = pd.read_csv('./data/weather_2018.csv')
    df_2019 = pd.read_csv('./data/weather_2019.csv')

    # Combine multiple years of weather data into one df
    weather_data_combined = pd.concat([df_2017, df_2018, df_2019], ignore_index=True)
    
    # Convert DataFrame to CSV file
    csv_buffer = io.StringIO()
    weather_data_combined.to_csv(csv_buffer, index=False)

    # Save CSV buffer to a temporary file
    temp_csv_file = '/tmp/temp.csv'
    with open(temp_csv_file, 'w') as f:
        f.write(csv_buffer.getvalue())

    # Upload the CSV file to the GCP bucket
    upload_to_gcp('data_bucket_raw', temp_csv_file, 'weather_data.csv')

    return weather_data_combined