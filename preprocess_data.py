import pandas as pd

def preprocess_energy(energy_data):
    # Rename the date column so that we can properly use it
    energy_data = energy_data.rename(columns={"Unnamed: 0": "date"})

    # Drop 2 unnecessary columns
    energy_data = energy_data.drop(["Elec_kW", "Gas_mxm"], axis=1)

    # Transform the cumulative power column into power generated per day
    energy_data['daily_power'] = energy_data['cum_power'].diff(periods=1)

    # Drop the cumulative power column as it is not necessary anymore now
    energy_data = energy_data.drop(["cum_power"], axis=1)
    return energy_data

def preprocess_weather(weather_data):
    # Precipitation, snow and tsun are always nan so we drop these 2 columns
    weather_data = weather_data.drop(["prcp", "snow", "tsun",
                                      "wdir", "wspd", "wpgt",
                                      "pres"], axis=1)
    return weather_data

def preprocess_data(weather_data, energy_data):
    # Preprocess weather and energy data individually
    energy_data = preprocess_energy(energy_data)
    weather_data = preprocess_weather(weather_data)

    # Merge energy data onto weather data based on the date
    data = weather_data.merge(energy_data, on="date")

    # Drop NAs
    data = data.dropna()
    return data

def preprocess_api_forecast_data(json_data):
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
    forecast_df = forecast_df.rename(columns = {"maxtemp_c": "tmax",
                                      "mintemp_c": "tmin",
                                      "avgtemp_c": "tavg"})
    forecast_df["date"] = dates
    return forecast_df