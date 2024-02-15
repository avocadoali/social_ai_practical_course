import pandas as pd
import numpy as np
from .preprocessing import preprocess_vehicle_data, calculate_mean_of_last_frames
def detect_exiting_vehicles(data):
    """
    Detect vehicles that are exhibiting exiting behavior based on certain conditions.

    :param data: DataFrame containing the dataset.
    :return: A DataFrame with exiting vehicles marked.
    """

    # Define thresholds for exiting behavior
    speed_threshold = 0.5  # Adjust based on your specific criteria
    last_frames_threshold = 5  # Check the last 5 frames for each vehicle
    lane_change_threshold = 0.9  # Threshold for considering lane change towards exit

    ############################# Preprocessing ################################

    data = preprocess_vehicle_data(data)

    ############################################################################

    # Create a new column to identify exiting vehicles
    data['is_exiting'] = False

    # Group by recordingId and trackId to process each vehicle's data individually
    for (recordingId, trackId), group in data.groupby(['recordingId', 'trackId']):
        # Sort by frame to ensure we are looking at the last frames
        sorted_group = group.sort_values(by='frame')

        # Check if the vehicle has a significant decrease in longitudinal velocity towards the end
        lon_vel_decreasing = calculate_mean_of_last_frames(sorted_group['lonVelocity'], last_frames_threshold) < speed_threshold

        # Check if the vehicle is moving laterally towards the lane edge
        moving_to_lane_edge = (sorted_group['latLaneCenterOffset'].abs() / sorted_group['laneWidth']).mean() > lane_change_threshold

        # Check if a lane change is happening towards the end of the track lifetime
        lane_changing = sorted_group.tail(last_frames_threshold)['laneChange'].any()

        # Check if the vehicle has traveled the full length of the lanelet
        full_lanelet_traveled = (sorted_group['traveledDistance'] >= sorted_group['laneletLength']).any()

        # If the vehicle is showing signs of exiting, mark as exiting

        if lon_vel_decreasing or (moving_to_lane_edge and lane_changing) or full_lanelet_traveled:
            data.loc[sorted_group.index, 'is_exiting'] = True

    return data
