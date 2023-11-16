import json
import logging
import os
from datetime import date
import requests


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_train_test_data(data):
    # Split the data statically after 80% into train and test
    split_idx = int(len(data) * 0.8)
    train_data = data.iloc[:split_idx]
    test_data = data.iloc[split_idx:]

    feature_columns = ["tavg", "tmin", "tmax"]
    target_columns = ["daily_power"]

    # Separate features (temperature) and target (solar energy)
    X_train = train_data[feature_columns]
    y_train = train_data[target_columns]
    X_test = test_data[feature_columns]
    y_test = test_data[target_columns]

    return X_train, y_train, X_test, y_test

def query_weather_from_api(city="London", n_days=3, reload=False):
    # Create file name for json data
    file_name = f"downloaded_api_data/{city}{n_days}{date.today()}.json"

    # Check if the file already exists
    if not reload and os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)

    # If reload is True or file doesn't exist, fetch data from the API
    response_dict = fetch_weather_details(city, n_days)

    # Save the fetched data
    with open(file_name, 'w') as file:
        json.dump(response_dict, file)

    return response_dict

def fetch_weather_details(city = "London", n_days = 3):
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

    querystring = {"q": city,
                   "days": str(n_days)}

    headers = {
        "X-RapidAPI-Key": "5abfd01e2fmsh0b56e60f2ced30ep16e1c9jsn58df4bd5501c",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    try:
        logger.info(f"Doing an API call to end-point {url}")
        response_text = requests.get(url, headers=headers, params=querystring)
        logger.info(f"Fetched API response {response_text}")
        response_dict = response_text.json()
        print(response_dict)
        return response_dict
    except Exception as ex:
        logger.info(f"Error while fetching weather details with Exception {ex}")#

