import pandas as pd


def filter_merge_onto_exit_ramps(data, exit_ramp_zones, speed_threshold):
    """
    Filters the data for merging onto exit ramp behavior based on predefined exit ramp zones and a speed threshold.

    Parameters:
    data (pandas.DataFrame): The dataset to filter.
    exit_ramp_zones (list of tuple): A list of tuples where each tuple defines an exit ramp zone
                                     with the format (exit_x_start, exit_x_end, exit_y_start, exit_y_end).
    speed_threshold (float): The speed threshold below which an object is considered to be merging onto an exit ramp.

    Returns:
    pandas.DataFrame: A new DataFrame containing only the data for objects merging onto exit ramps.
    """
    # Create an empty DataFrame to store the filtered data
    merge_data = pd.DataFrame()

    # Get unique times and ids from the data
    unique_times = data['time'].unique()
    unique_ids = data['id'].unique()

    for time in unique_times:
        time_data = data[data['time'] == time]

        for obj_id in unique_ids:
            obj_data = time_data[time_data['id'] == obj_id]

            # Check if object is within an exit ramp zone and has reduced speed
            for zone in exit_ramp_zones:
                if (zone[0] <= obj_data['x'].values[0] <= zone[1] and
                        zone[2] <= obj_data['y'].values[0] <= zone[3] and
                        obj_data['speed'].values[0] < speed_threshold):
                    merge_data = pd.concat([merge_data, obj_data])

    return merge_data