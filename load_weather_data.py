import pandas as pd

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
    weather_data_combined = pd.concat([df_2017, df_2018, df_2019],
                                      ignore_index=True)
    return weather_data_combined