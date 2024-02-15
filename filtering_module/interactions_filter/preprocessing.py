import pandas as pd
import numpy as np
import re

def parse_string_to_array(s):
    # Use a regular expression to find all numbers in the string
    numbers = re.findall(r'-?\d+\.?\d*', s)
    # Convert the found numbers to floats (or integers if needed)
    return np.array(numbers, dtype=float)

def convert_column_to_array(data, column_name):
    # Convert the column to string type
    data[column_name] = data[column_name].astype(str)

    # Apply the parsing function to the specified column
    data[column_name] = data[column_name].apply(parse_string_to_array)
    return data


def calculate_mean_of_last_frames(series, threshold):
    # This assumes the series contains lists of numbers and we want the mean of the last `threshold` numbers in each list
    means = series.apply(lambda x: np.mean(x[-threshold:]) if isinstance(x, list) and len(x) >= threshold else np.nan)
    return means.mean()

def calculate_mean_of_first_frames(series, threshold):
    # This assumes the series contains lists of numbers and we want the mean of the first `threshold` numbers in each list
    means = series.apply(lambda x: np.mean(x[:threshold]) if isinstance(x, list) and len(x) >= threshold else np.nan)
    return means.mean()
def clean_lane_change_column(dataframe):
    # Convert laneChange to numeric, setting errors='coerce' to convert non-numeric values to NaN
    dataframe['laneChange'] = pd.to_numeric(dataframe['laneChange'], errors='coerce')
    # Replace NaN values with 0 (no lane change)
    dataframe['laneChange'] = dataframe['laneChange'].fillna(0)
    # Ensure the column is of integer type
    dataframe['laneChange'] = dataframe['laneChange'].astype(int)
    return dataframe


def check_column_structure(data):
    # Ensure that traveledDistance and laneletLength are not lists or arrays
    def fix_traveled_distance(x):
        if isinstance(x, (list, np.ndarray)):
            return x[0]
        return x

    def fix_lanelet_length(x):
        if isinstance(x, (list, np.ndarray)):
            # Ensure we have a 1D array to work with
            x = np.array(x).ravel()
            # Filter out the NaN values and get the first element
            filtered = [item for item in x if not np.isnan(item)]
            return filtered[0] if filtered else np.nan
        return x

    data['traveledDistance'] = data['traveledDistance'].apply(fix_traveled_distance)
    data['laneletLength'] = data['laneletLength'].apply(fix_lanelet_length)

    # Let's add a check here to make sure the values are correctly formatted
    assert all(isinstance(x, (int, float, np.integer, np.floating)) for x in
               data['traveledDistance']), "traveledDistance contains non-scalar values"
    assert all(isinstance(x, (int, float, np.integer, np.floating)) for x in
               data['laneletLength']), "laneletLength contains non-scalar values"

    return data

def check_array_elements(dataframe):
    first_traveled_distance = dataframe['traveledDistance'].iloc[0]
    first_lanelet_length = dataframe['laneletLength'].iloc[0]


def preprocess_vehicle_data(data):
    """
    Preprocess the vehicle data for analysis.

    :param data: DataFrame containing the dataset.
    :return: Preprocessed DataFrame.
    """
    # Convert columns to numeric, setting errors='coerce' will replace non-numeric values with NaN
    numeric_cols = ['latLaneCenterOffset', 'laneWidth', 'laneletId', 'lonLaneletPos', 'laneletLength']
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # Check for rows where any of these columns have NaN values after conversion
    non_numeric_rows = data[numeric_cols].isnull().any(axis=1)

    # Remove rows with invalid recordingId (e.g., containing ';;;;;')
    data_cleaned = data[data['recordingId'].apply(lambda x: str(x).isdigit())]

    # Remove rows with NaN values in any of the specified columns
    data_cleaned = data_cleaned.dropna(subset=numeric_cols)

    # Convert the 'trackId' column to numeric as well, because it should be an identifier for the tracks
    data_cleaned['trackId'] = pd.to_numeric(data_cleaned['trackId'], errors='coerce')

    # Drop rows with NaN in 'trackId' after conversion
    data_cleaned = data_cleaned.dropna(subset=['trackId'])

    # Reset index after row removal
    data_cleaned.reset_index(drop=True, inplace=True)

    # Check the data info again to ensure clean data
    data_cleaned.info()

    # Convert 'recordingId' and 'frame' columns to numeric
    data_cleaned['recordingId'] = pd.to_numeric(data_cleaned['recordingId'], errors='coerce')
    data_cleaned['frame'] = pd.to_numeric(data_cleaned['frame'], errors='coerce')

    # Drop rows with NaN in 'recordingId' and 'frame' after conversion
    data_cleaned = data_cleaned.dropna(subset=['recordingId', 'frame'])

    # Rename the last column to remove invalid characters
    data_cleaned.rename(columns={'odrLaneId;;;;;': 'odrLaneId'}, inplace=True)

    # Convert 'odrLaneId' to numeric as well
    data_cleaned['odrLaneId'] = pd.to_numeric(data_cleaned['odrLaneId'], errors='coerce')

    # Check the data info again to ensure clean data
    data_cleaned.info()

    # Also show the first few rows to verify the changes
    data_cleaned.head()

    # Convert 'xCenter' and 'yCenter' columns to numeric
    data_cleaned['xCenter'] = pd.to_numeric(data_cleaned['xCenter'], errors='coerce')
    data_cleaned['yCenter'] = pd.to_numeric(data_cleaned['yCenter'], errors='coerce')

    # Drop rows with NaN in 'xCenter' and 'yCenter' after conversion
    data_cleaned = data_cleaned.dropna(subset=['xCenter', 'yCenter'])

    data = clean_lane_change_column(data)
    check_column_structure(data)
    check_array_elements(data)

    # data = convert_column_to_array(data, 'frame')
    data = convert_column_to_array(data, 'xCenter')
    data = convert_column_to_array(data, 'yCenter')

    return data

def flatten_list_of_arrays(lst):
    """ Flatten a list of numpy arrays into a single list """
    return [item for sublist in lst for item in sublist]

def filter_float_in_series_of_lists(series, float_value):
    """
    Creates a boolean mask for a Pandas Series (whose elements are lists or arrays) to indicate
    whether a specific floating-point value is present in each list or array.
    series (pd.Series): The Pandas Series to be filtered.
    float_value (float): The floating-point value to filter for.
    Returns:
    pd.Series: A boolean Series indicating whether each list or array in the original series contains the float_value.
    """
    return series.apply(lambda lst: float_value in lst)