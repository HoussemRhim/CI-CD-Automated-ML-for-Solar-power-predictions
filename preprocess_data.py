import os
import pandas as pd
from google.cloud import storage


# Set the project ID
PROJECT_ID = "reflected-oath-405515"
# Set the path to your JSON credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./reflected-oath-405515-70b04b6190ad.json"

def download_from_gcs(bucket_name, blob_name):
    """Downloads a DataFrame from Google Cloud Storage."""
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    data = blob.download_as_text()
    return pd.read_csv(pd.compat.StringIO(data))

def upload_to_gcs(data, bucket_name, blob_name):
    """Uploads a DataFrame to Google Cloud Storage."""
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data.to_csv(index=False), 'text/csv')
    
def preprocess_energy(bucket_name, energy_blob_name):
    # Download energy data from GCS
    energy_data = download_from_gcs('data_bucket_raw', 'energy_data.csv')
    
    # Rename the date column so that we can properly use it
    energy_data = energy_data.rename(columns={"Unnamed: 0": "date"})

    # Drop 2 unnecessary columns
    energy_data = energy_data.drop(["Elec_kW", "Gas_mxm"], axis=1)

    # Transform the cumulative power column into power generated per day
    energy_data['daily_power'] = energy_data['cum_power'].diff(periods=1)

    # Drop the cumulative power column as it is not necessary anymore now
    energy_data = energy_data.drop(["cum_power"], axis=1)
    
    return energy_data

def preprocess_weather(bucket_name, weather_blob_name):
    # Download weather data from GCS
    weather_data = download_from_gcs('data_bucket_raw', 'weather_data.csv')
    
    # Precipitation, snow and tsun are always nan so we drop these 2 columns
    weather_data = weather_data.drop(["prcp", "snow", "tsun", "wdir", "wspd", "wpgt", "pres"], axis=1)
    
    return weather_data

def preprocess_data(bucket_name, energy_blob_name, weather_blob_name):
    # Preprocess weather and energy data individually
    energy_data = preprocess_energy(bucket_name, energy_blob_name)
    weather_data = preprocess_weather(bucket_name, weather_blob_name)

    # Merge energy data onto weather data based on the date
    data = weather_data.merge(energy_data, on="date")

    # Drop NAs
    data = data.dropna()

    # Upload the processed data to GCS
    upload_to_gcs(data, 'data_bucket_processed', 'data')

    return data

def preprocess_api_forecast_data(json_data, output_blob_name):
    # We only need the daily forecast from the json payload
    forecast = json_data["forecast"]["forecastday"]

    # We extract the date and temperatures from each forecast day
    dates = [key["date"] for key in forecast]
    days = [key["day"] for key in forecast]

    # Create a df from those datapoints
    forecast_df = pd.DataFrame.from_dict(days)

    # Just take the temperature columns
    forecast_df = forecast_df[["maxtemp_c", "mintemp_c", "avgtemp_c"]]

    # Rename to the same names as in the csv data
    forecast_df = forecast_df.rename(columns = {"maxtemp_c": "tmax", "mintemp_c": "tmin", "avgtemp_c": "tavg"})

    forecast_df["date"] = dates
    
    # Upload the processed forecast data to GCS
    upload_to_gcs(forecast_df, 'data_bucket_processed', 'processed_forecast_data.csv')

    return forecast_df