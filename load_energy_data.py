import pandas as pd

def load_energy_data_from_csv():
    """
    Helper function to load electricity data from disk

    Solar energy data found on kaggle:
    https://www.kaggle.com/datasets/fvcoppen/solarpanelspower/code?select=metingen_27feb2022.csv
    
    :return: loaded pandas df
    """

    # Load CSV file into a DataFrame
    df = pd.read_csv('data/PV_Elec_Gas2.csv')
    return df