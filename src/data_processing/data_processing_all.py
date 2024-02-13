import os
import pandas as pd
import numpy as np
from loguru import logger
from src.data_processing.tracks_import import read_from_csv
from src.utils.load_config import load_config

def process_data(dataset_dir_raw, recording, output_directory):
    # Check if the directory exists
    if not os.path.isdir(dataset_dir_raw):
        print(dataset_dir_raw)
        raise Exception("Directory does not exist")

    # Create paths to csv files
    print(recording)
    tracks_file = os.path.join(dataset_dir_raw, recording + "_tracks.csv")
    tracks_meta_file = os.path.join(dataset_dir_raw, recording + "_tracksMeta.csv")
    recording_meta_file = os.path.join(dataset_dir_raw, recording + "_recordingMeta.csv")

    # Check if the files exist
    if not all(os.path.isfile(file) for file in [tracks_file, tracks_meta_file, recording_meta_file]):
        raise Exception("One or more files do not exist")

    # Load csv files
    logger.info("Loading csv files {}, {} and {}", tracks_file, tracks_meta_file, recording_meta_file)
    tracks, static_info, meta_info = read_from_csv(tracks_file, tracks_meta_file, recording_meta_file,
                                                   include_px_coordinates=True)
    df_tracks = pd.DataFrame(tracks)
    df_static_info = pd.DataFrame(static_info)
    df_meta_info = pd.DataFrame(meta_info.items())
    #display(df_tracks)

    n = len(df_tracks)

    track_ids = list(range(n))  

    selected_tracks = df_tracks[df_tracks['trackId'].isin(track_ids)]

    # Change the position to the distance by subtracting the starting position from the position lists
    selected_tracks.loc[:, 'xCenter'] = selected_tracks['xCenter'].apply(lambda num: [x - num[0] for x in num[:]])
    selected_tracks.loc[:, 'yCenter'] = selected_tracks['yCenter'].apply(lambda num: [x - num[0] for x in num[:]])

    # Select distance, velocity, and acceleration columns
    columns_to_select = ['xCenter', 'yCenter', 'xVelocity', 'yVelocity', 'xAcceleration', 'yAcceleration']
    selected_data = selected_tracks[columns_to_select]

    # Unstack the selected_data DataFrame to flatten the lists in the 'xCenter', 'yCenter', etc. columns
    selected_data_unstacked = selected_data.apply(lambda x: np.concatenate(x.values))

    # Create a new DataFrame
    new_dataframe = pd.DataFrame(selected_data_unstacked)
    #display(new_dataframe)

    # Create processed_data_path if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    file_name = f'x_y_recording_{recording}_range_{n}.csv'
    output_file_path = os.path.join(output_directory, file_name)

    # Save the new_dataframe as a CSV file in the data/processed directory
    print(output_file_path)
    new_dataframe.to_csv(output_file_path, index=False)

def main():
    config = load_config()['data']

    raw_data_path_ind = config['raw_data_path_ind']
    processed_data_path_ind = config['processed_data_path_ind']
    number_of_recordings = config['number_of_recordings']

    for i in range(number_of_recordings):
        recording = str(i).zfill(2)
        process_data(raw_data_path_ind, str(recording), processed_data_path_ind)


if __name__ == "__main__":
    main()