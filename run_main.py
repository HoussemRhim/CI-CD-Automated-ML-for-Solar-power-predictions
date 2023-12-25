from helper_functions import query_weather_from_api
from helper_functions import get_train_test_data
from load_energy_data import load_energy_data_from_csv
from load_weather_data import load_weather_data
from preprocess_data import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from google.cloud import storage


# Set the project ID
PROJECT_ID = "reflected-oath-405515"
# Set the path to your JSON credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./terraform/reflected-oath-405515-70b04b6190ad.json"

def download_from_gcs(bucket_name, blob_name):
    """Downloads a DataFrame from Google Cloud Storage."""
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    file_data = blob.download_as_text()
    return pd.read_csv(pd.compat.StringIO(file_data))


# Preprocessing to join the data frames into one and do some cleaning
data = preprocess_data('data_bucket_raw', 'energy_data.csv', 'weather_data.csv')

# Load data directly from GCS:
#weather_data = download_from_gcs('data_bucket_processed', 'weather_data.csv')
#energy_data = download_from_gcs('data_bucket_processed', 'energy_data.csv')
# Load data:
#weather_data = load_weather_data()
#energy_data = load_energy_data_from_csv()


# Split into train and test data
X_train, y_train, X_test, y_test = get_train_test_data(data)

# Initialize and train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict solar energy for the test set
y_pred = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)

print(f'Mean Absolute Error: {mae}')



#Predict new data
future_data = query_weather_from_api("Antwerp", 3, False)
future_data = preprocess_api_forecast_data(future_data, 'processed_forecast_data.csv')
print(future_data)
print(model.predict(future_data[["tavg", "tmin", "tmax"]]))