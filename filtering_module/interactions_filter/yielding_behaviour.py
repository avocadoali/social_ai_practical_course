# This model is deprecated and serves as an example. Please use the new model inside the entering_behaviour.py.
# It is integrated into entering behaviour function due to runtime optimizatiton.

import pandas as pd


def filter_yielding_behaviour(data, yielding_threshold=10):
    """
    Filters the data for yielding behavior based on a specified speed reduction threshold.

    Parameters:
    data (pandas.DataFrame): The dataset to filter.
    yielding_threshold (float): The speed reduction threshold for yielding. Defaults to 10.
    """
    # Create an empty DataFrame to store the filtered data
    yielding_data = pd.DataFrame()

    # Get unique times and ids from the data
    unique_times = data['time'].unique()
    unique_ids = data['id'].unique()

    for time in unique_times:
        time_data = data[data['time'] == time]

        for obj_id in unique_ids:
            obj_data = time_data[time_data['id'] == obj_id]

            # Check if object has reduced speed significantly
            previous_time_data = data[(data['time'] == time - 1) & (data['id'] == obj_id)]
            if not previous_time_data.empty and (
                    previous_time_data['speed'].values[0] - obj_data['speed'].values[0] > yielding_threshold):
                yielding_data = pd.concat([yielding_data, obj_data])

    return yielding_data