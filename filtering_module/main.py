from interactions_filter import InteractionsFilter
from utilities import load_exid_data, load_round_data, load_inD_data, read_all_recordings_from_csv, read_from_csv, read_tracks, read_tracks_meta, read_recording_meta, get_rotated_bbox

from loguru import logger
from typing import List

import pandas as pd
import numpy as np
import os

# Specify the paths
dataset_dir = "data/exid/"
recording = 83 #16



def process_and_export_car_data(distance_info, current_car_csv_path, other_car_csv_path):
    """
        Process and export car data to CSV files.
        Args:
        - distance_info: List of dictionaries containing distance information between cars.
        - current_car_csv_path: File path to export data related to the current car.
        - other_car_csv_path: File path to export data related to other cars.
        """
    # Initializing lists to store data for the current car and the other car
    current_car_data = []
    other_car_data = []

    # Make sure the base path exists
    os.makedirs("csv_files/", exist_ok=True)

    # Iterate through the list of dictionaries
    for data_dict in distance_info:
        # Iterate through each key-value pair in the dictionary
        for pair_key, data_list in data_dict.items():
            # Iterate through the list of data tuples
            for data_tuple in data_list:
                # Unpack the data tuple
                recordingId, current_trackId, other_trackId, frame, distance, current_x_vel, current_y_vel, other_x_vel, other_y_vel, current_x_accel, current_y_accel, other_x_accel, other_y_accel, current_x_center, current_y_center, other_x_center, other_y_center = data_tuple

                # Append data for the current car
                current_car_data.append({
                    'RecordingId': recordingId,
                    'TrackId': current_trackId,
                    'Frame': frame,
                    'Distance': distance,
                    'XVelocity': current_x_vel,
                    'YVelocity': current_y_vel,
                    'XAcceleration': current_x_accel,
                    'YAcceleration': current_y_accel,
                    'XCenter': current_x_center,
                    'YCenter': current_y_center
                })

                # Append data for the other car
                other_car_data.append({
                    'RecordingId': recordingId,
                    'TrackId': other_trackId,
                    'Frame': frame,
                    'Distance': distance,
                    'XVelocity': other_x_vel,
                    'YVelocity': other_y_vel,
                    'XAcceleration': other_x_accel,
                    'YAcceleration': other_y_accel,
                    'XCenter': other_x_center,
                    'YCenter': other_y_center
                })

    # Convert lists to DataFrames
    current_car_df = pd.DataFrame(current_car_data)
    other_car_df = pd.DataFrame(other_car_data)

    # Export to CSV files
    current_car_df.to_csv(os.path.join("csv_files/", current_car_csv_path), index=False)
    other_car_df.to_csv(os.path.join("csv_files/", other_car_csv_path), index=False)

    print(f"Data exported to {current_car_csv_path} and {other_car_csv_path}")



def process_single_recording(recording_id, dataset_dir):
    """
        Process data for a single recording.

        Args:
        - recording_id: ID of the recording.
        - dataset_dir: Directory containing the dataset.
        """
    # Format recording_id with leading zero if it's less than 10
    formatted_recording_id = f"{recording_id:02d}"  # This will add a leading zero for single-digit numbers

    # Create paths to csv files for the specific recording
    tracks_file = f"{dataset_dir}{formatted_recording_id}_tracks.csv"
    tracks_meta_file = f"{dataset_dir}{formatted_recording_id}_tracksMeta.csv"
    recording_meta_file = f"{dataset_dir}{formatted_recording_id}_recordingMeta.csv"

    # Load the data for the recording
    logger.info(f"Loading csv files {tracks_file}, {tracks_meta_file}, and {recording_meta_file}")
    tracks, static_info, meta_info = read_from_csv(tracks_file, tracks_meta_file, recording_meta_file,
                                                   include_px_coordinates=True)

    df_tracks = pd.DataFrame(tracks)
    df_static_info = pd.DataFrame(static_info)
    df_meta_info = pd.DataFrame(meta_info.items())

    # Print data for debugging (optional)
    # with pd.option_context('display.max_rows', 4, 'display.max_columns', 3, 'display.precision', 3):
    #     print(df_tracks)

    # Create an instance of InteractionsFilter
    interactions_filter = InteractionsFilter()

    # Perform the filtering operations for the recording
    exiting_behavior_data = interactions_filter.detect_exiting_vehicles(df_tracks)
    entering_behavior_data, all_distance_info_filtered = interactions_filter.detect_entering_vehicles(df_tracks, interaction_distance_threshold=10,
                                                                          relative_speed_threshold=0.5, tailgating_distance_threshold=5, yielding_speed_threshold=1, yielding_distance_threshold=5)
    # overtaking_behavior_data = interactions_filter.detect_overtaking(df_tracks, interaction_distance_threshold=10, relative_speed_threshold=0.5, position_change_threshold=0.9)


    # This prints serves as a check for the filtering operation
    print("These are the cars getting closer and having interaction")
    print(all_distance_info_filtered)

    # Check and print information about exiting and entering vehicles
    exiting_exists = check_for_exiting_vehicles(df_tracks)
    entering_exists = check_for_entering_vehicles(df_tracks)
    print_exiting_vehicle_ids(df_tracks)
    print_entering_vehicle_ids(df_tracks)

    # Define the file name
    file_name = 'data.txt'

    # Open the file in write mode and write the data
    with open(file_name, 'w') as file:
        for data in all_distance_info_filtered:
            # Convert each tuple to a string and write it to the file
            file.write(str(data) + '\n')
    process_and_export_car_data(all_distance_info_filtered, f'current_car_data_{recording}.csv', f'other_car_data_{recording}.csv')

    # These functions are for specific types of interactions
    # merge_onto_exit_ramps_data = interactions_filter.filter_merge_onto_exit_ramps(exid_data)
    # yielding_behavior_data = interactions_filter.filter_yielding_behavior(exid_data)
    # speed_adjustment_data = interactions_filter.filter_speed_adjustment(exid_data)
    # merging_and_lane_changing_data = interactions_filter.filter_merging_and_lane_changing(exid_data)

    # You can return data if needed for further processing
    return exiting_behavior_data, entering_behavior_data

def print_exiting_vehicle_ids(data):
    # Filter the DataFrame for rows where 'is_exiting' is True
    exiting_vehicles = data[data['is_exiting'] == True]

    # Get the unique IDs of these vehicles
    exiting_vehicle_ids = exiting_vehicles['trackId'].unique()

    # Print out the IDs
    for vehicle_id in exiting_vehicle_ids:
        print(f'Car with ID {vehicle_id} is exiting.')

    # If you need the list of IDs for further processing, you can return it
    return exiting_vehicle_ids

def print_entering_vehicle_ids(data):
    # Filter the DataFrame for rows where 'is_entering' is True
    entering_vehicles = data[data['is_entering'] == True]

    # Get the unique IDs of these vehicles
    entering_vehicle_ids = entering_vehicles['trackId'].unique()

    # Print out the IDs
    for vehicle_id in entering_vehicle_ids:
        print(f'Car with ID {vehicle_id} is entering.')

    # If you need the list of IDs for further processing, you can return it
    return entering_vehicle_ids

def check_for_exiting_vehicles(data):
    # Check if there's any 'True' in the 'is_exiting' column
    has_exiting_vehicles = data['is_exiting'].any()

    # Print result and return
    if has_exiting_vehicles:
        print("There are vehicles exiting.")
    else:
        print("There are no vehicles exiting.")

    return has_exiting_vehicles

def check_for_entering_vehicles(data):
    # Check if there's any 'True' in the 'is_exiting' column
    has_entering_vehicles = data['is_entering'].any()

    # Print result and return
    if has_entering_vehicles:
        print("There are vehicles entering.")
    else:
        print("There are no vehicles entering.")

    return has_entering_vehicles

def main():
    process_single_recording(recording, dataset_dir)

    file_name = 'data.txt'

    # Initialize an empty list to store the data
    data_from_file = []

    # Open the file and read each line
    with open(file_name, 'r') as file:
        for line in file:
            # Evaluate each line as a tuple and append to the list
            # strip() is used to remove newline characters and spaces
            data_from_file.append(eval(line.strip()))

    process_and_export_car_data(data_from_file, 'current_car_data.csv', 'other_car_data.csv')

    # This is for using the function for all recordings / You need to remove comments to use this
    # for recording in range(0, 93):  # Loop through all recordings from 0 to 92
    #     process_single_recording(recording, dataset_dir)

if __name__ == "__main__":
    main()