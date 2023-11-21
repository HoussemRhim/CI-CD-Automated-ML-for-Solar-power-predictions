from helper_functions import query_weather_from_api
from helper_functions import get_train_test_data
from load_energy_data import load_energy_data_from_csv
from load_weather_data import load_weather_data
from preprocess_data import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from google.cloud import storage

# Load data directly from GCS:
weather_data = download_from_gcs('data_bucket_processed', 'weather_data')
energy_data = download_from_gcs('data_bucket_processed', 'energy_data')
# Load data:
#weather_data = load_weather_data()
#energy_data = load_energy_data_from_csv()

# Preprocessing to join the data frames into one and do some cleaning
data = preprocess_data(weather_data, energy_data)



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
future_data = preprocess_api_forecast_data(future_data)
print(future_data)
print(model.predict(future_data[["tavg", "tmin", "tmax"]]))