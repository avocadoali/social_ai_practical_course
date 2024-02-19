import pandas as pd
import numpy as np
from .preprocessing import preprocess_vehicle_data, calculate_mean_of_last_frames, calculate_mean_of_first_frames
from tqdm import tqdm

def detect_overtaking(data, interaction_distance_threshold=10, relative_speed_threshold=0.5, position_change_threshold=0.9):
    """
    Detect vehicles that are exhibiting entering or merging behavior based on certain conditions.
    :param data: DataFrame containing the dataset.
    :return: A DataFrame with entering vehicles marked.
    """

    # Define thresholds for entering behavior
    speed_increase_threshold = 0.5  # Adjust based on your specific criteria
    initial_frames_threshold = 5  # Check the first 5 frames for each vehicle
    lane_change_threshold = 0.9  # Threshold for considering lane change towards entry

    ############################# Preprocessing ################################

    data = preprocess_vehicle_data(data)

    ############################################################################
    # data.to_csv('Output.csv', index=False)
    # Create a new column to identify entering vehicles
    # Create a new column to identify entering vehicles

    # Group by recordingId and trackId
    grouped_data = data.groupby(['recordingId', 'trackId'])

    print("------------ Analyzing vehicles ------------")

    for (recordingId, trackId), group in tqdm(grouped_data, desc="Analyzing vehicles"):
    # for (recordingId, trackId), group in grouped_data:
        sorted_group = group.sort_values(by='frame')

        # Check for vehicle interaction and relative velocity
        close_vehicles_info = check_vehicle_interaction_and_relative_velocity(grouped_data, recordingId,
                                                                                           trackId,
                                                                                           interaction_distance_threshold,
                                                                                           relative_speed_threshold, position_change_threshold)

    return data

def check_vehicle_interaction_and_relative_velocity(grouped_data, current_recordingId, current_trackId, distance_threshold, speed_threshold, position_change_threshold):
    current_group = grouped_data.get_group((current_recordingId, current_trackId))
    all_frames = flatten_list_of_arrays(current_group['frame'].tolist())
    unique_frames = np.unique(all_frames)

    distance_info = {}
    overtaking_events = []

    for frame in unique_frames:
        frame_index = frame - unique_frames[0]
        current_frame_data = current_group[filter_float_in_series_of_lists(current_group['frame'], frame)]
        current_velocity = current_frame_data['lonVelocity'].values[0][frame_index] if not current_frame_data.empty else None

        for (recordingId, trackId), group in grouped_data:
            if recordingId == current_recordingId and trackId != current_trackId:
                other_frame_data = group[filter_float_in_series_of_lists(group['frame'], frame)]
                other_velocity = other_frame_data['lonVelocity'].values[0][frame - unique_frames[0]] if not other_frame_data.empty else None

                if not current_frame_data.empty and not other_frame_data.empty:
                    current_x_pos = current_frame_data['xCenter'].values[0][frame_index]
                    other_x_pos = other_frame_data['xCenter'].values[0][frame - unique_frames[0]]
                    distance = np.sqrt((current_x_pos - other_x_pos) ** 2 + (current_frame_data['yCenter'].values[0][frame_index] - other_frame_data['yCenter'].values[0][frame - unique_frames[0]]) ** 2)

                    lane_change = current_frame_data['laneChange'].values[0][frame_index] != 0 or other_frame_data['laneChange'].values[0][frame - unique_frames[0]] != 0
                    relative_position_change = current_x_pos - other_x_pos

                    if lane_change and distance < distance_threshold and abs(relative_position_change) > position_change_threshold:
                        relative_speed = abs(current_velocity - other_velocity)
                        if relative_speed > speed_threshold:
                            overtaking_events.append((current_trackId, trackId, frame))
                            print(f"Overtaking detected: Vehicle {current_trackId} overtook Vehicle {trackId} at frame {frame}")

                    if distance < distance_threshold:
                        pair_key = (current_trackId, trackId)
                        if pair_key not in distance_info:
                            distance_info[pair_key] = []
                        distance_info[pair_key].append((frame, distance))

    return overtaking_events, distance_info

# Helper function to filter floats in a series of lists
def filter_float_in_series_of_lists(series, float_value):
    return series.apply(lambda lst: float_value in lst)

def flatten_list_of_arrays(lst):
    """ Flatten a list of numpy arrays into a single list """
    return [item for sublist in lst for item in sublist]