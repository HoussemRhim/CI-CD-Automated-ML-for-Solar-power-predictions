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

def combine_and_upload_to_gcs(file_paths, bucket_name, destination_blob_name):
    """
    Combine multiple CSV files into one DataFrame and upload it to GCS.

    :param file_paths: List of paths to CSV files
    :param bucket_name: Name of the GCS bucket
    :param destination_blob_name: Name for the destination blob in GCS
    """
    try:
        # Combine CSV files into one DataFrame
        weather_data_combined = pd.concat([pd.read_csv(file) for file in file_paths], ignore_index=True)


        # Upload data to GCS bucket
        upload_to_gcs(weather_data_combined, bucket_name, destination_blob_name)

        print(f"Data uploaded to GCS: gs://{bucket_name}/{destination_blob_name}")

    except Exception as e:
        print(f"Error: {e}")
        raise  # Re-raise the exception to halt execution

def upload_to_gcs(data, bucket_name, file_name):
    """
    Upload a DataFrame to GCS.

    :param data: DataFrame to upload
    :param bucket_name: Name of the GCS bucket
    :param file_name: Name for the destination blob in GCS
    """
    
    try:
        # Get the path to the JSON credentials file
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        client = storage.Client(project=PROJECT_ID)
        bucket = client.get_bucket(bucket_name)

        # Convert DataFrame to CSV string
        csv_data = data.to_csv(index=False)

        # Write CSV string to a temporary file
        temp_file_name = "/tmp/temp_data.csv"
        with open(temp_file_name, 'w') as file:
            file.write(csv_data)

        # Upload the file to GCS
        blob = bucket.blob(file_name)
        blob.upload_from_filename(temp_file_name)

        # Remove the temporary file
        os.remove(temp_file_name)

    except Exception as e:
        print(f"Error: {e}")
        raise  # Re-raise the exception to halt execution

def load_weather_data():
   
# List of paths to CSV files
    file_paths = ['./data/weather_2017.csv', './data/weather_2018.csv', './data/weather_2019.csv']

# Destination blob name in GCS
    destination_blob_name = 'weather_data.csv'

    # Upload data to GCS bucket
    combine_and_upload_to_gcs(file_paths, 'data_bucket_raw', destination_blob_name)

    # Load the combined data from GCS
    weather_data_combined = pd.read_csv(f'gs://data_bucket_raw/{destination_blob_name}')

    return weather_data_combined


    
