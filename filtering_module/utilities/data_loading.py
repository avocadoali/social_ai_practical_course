import pandas as pd

def load_exid_data(filepath='exid.csv'):
    """
    Loads the exid dataset from a CSV file.

    Parameters:
    filepath (str): The path to the CSV file. Defaults to 'exid.csv'.

    Returns:
    pandas.DataFrame: The loaded exid dataset.
    """
    try:
        exid_data = pd.read_csv(filepath)
        return exid_data
    except Exception as e:
        print(f"An error occurred while loading the exid dataset: {e}")
        return None

def load_round_data(filepath='round.csv'):
    """
    Loads the round dataset from a CSV file.

    Parameters:
    filepath (str): The path to the CSV file. Defaults to 'round.csv'.

    Returns:
    pandas.DataFrame: The loaded round dataset.
    """
    try:
        round_data = pd.read_csv(filepath)
        return round_data
    except Exception as e:
        print(f"An error occurred while loading the round dataset: {e}")
        return None

def load_inD_data(filepath='inD.csv'):
    """
    Loads the inD dataset from a CSV file.

    Parameters:
    filepath (str): The path to the CSV file. Defaults to 'inD.csv'.

    Returns:
    pandas.DataFrame: The loaded inD dataset.
    """
    try:
        inD_data = pd.read_csv(filepath)
        return inD_data
    except Exception as e:
        print(f"An error occurred while loading the inD dataset: {e}")
        return None



