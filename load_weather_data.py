import os
import pandas as pd
from google.cloud import storage
import io

# Set the project ID
PROJECT_ID = "reflected-oath-405515"
# Set the path to your JSON credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./terraform/reflected-oath-405515-70b04b6190ad.json"

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
    temp_csv_file = './data/temp.csv'
    with open(temp_csv_file, 'w') as f:
        f.write(csv_buffer.getvalue())

    # Upload the CSV file to the GCP bucket
    upload_to_gcp('data_bucket_raw', temp_csv_file, 'weather_data.csv')

    return weather_data_combined


if __name__ == "__main__":
    # Modify the arguments based on your specific use case
    load_weather_data('data_bucket_raw', 'weather_data.csv')