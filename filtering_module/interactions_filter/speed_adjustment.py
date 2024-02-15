import pandas as pd


def filter_speed_adjustment(data, speed_change_threshold=10):
    """
    Filters the data for speed adjustment behavior based on a specified speed change threshold.

    Parameters:
    data (pandas.DataFrame): The dataset to filter.
    speed_change_threshold (float): The speed change threshold for identifying speed adjustment. Defaults to 10.

    Returns:
    pandas.DataFrame: A new DataFrame containing only the data for objects exhibiting speed adjustment behavior.
    """
    # Create an empty DataFrame to store the filtered data
    speed_adjustment_data = pd.DataFrame()

    # Get unique times and ids from the data
    unique_times = data['time'].unique()
    unique_ids = data['id'].unique()

    for time in unique_times:
        time_data = data[data['time'] == time]

        for obj_id in unique_ids:
            obj_data = time_data[time_data['id'] == obj_id]

            # Check if object has changed speed significantly
            previous_time_data = data[(data['time'] == time - 1) & (data['id'] == obj_id)]
            if not previous_time_data.empty and (
                    abs(previous_time_data['speed'].values[0] - obj_data['speed'].values[0]) > speed_change_threshold):
                speed_adjustment_data = pd.concat([speed_adjustment_data, obj_data])

    return speed_adjustment_data