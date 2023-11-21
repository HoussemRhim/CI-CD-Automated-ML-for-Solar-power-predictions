import pandas as pd
from google.cloud import storage

def load_weather_data():
    """
    Helper function to load weather data

    Downloaded from publicly available weather data from https://meteostat.net/
    For the city of Antwerp (2011-Today)

    :return: loaded pandas df
    """

    # Load each year file of data
    df_2017 = pd.read_csv('data/weather_2017.csv')
    df_2018 = pd.read_csv('data/weather_2018.csv')
    df_2019 = pd.read_csv('data/weather_2019.csv')

    # Combine multiple years of weather data into one df
    weather_data_combined = pd.concat([df_2017, df_2018, df_2019], ignore_index=True)

    # Upload data to GCS bucket
    upload_to_gcs(weather_data_combined, 'data_bucket_raw', 'weather_data.csv')

    return weather_data_combined

def upload_to_gcs(data, bucket_name, file_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    # Convert DataFrame to CSV string
    csv_data = data.to_csv(index=False)

    # Upload CSV string to GCS
    blob = bucket.blob(file_name)
    blob.upload_from_string(csv_data, content_type='text/csv')