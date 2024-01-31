import pandas as pd
import shutil

# Get one car from tracks.csv 
df = pd.read_csv('data/raw/inD/data/00_tracks.csv')
track_one_car = df[df['trackId']== 6]
track_vis_path = 'data/processed/visualization_data/ground_truth/00_tracks.csv'
track_one_car.to_csv(track_vis_path)

# Get that one car from trackMeta.csv
tracks_meta = pd.read_csv('data/raw/inD/data/00_tracksMeta.csv')
tracks_meta_new = tracks_meta[tracks_meta['trackId'] == 6]
tracks_meta_file = 'data/processed/visualization_data/ground_truth/00_tracksMeta.csv'
tracks_meta_new.to_csv(tracks_meta_file)

# Copying Meta other data 
background_path = 'data/raw/inD/data/00_background.png'
recording_meat_path = 'data/raw/inD/data/00_recordingMeta.csv'
dst_path = 'data/processed/visualization_data/ground_truth'
dst_path_pred = 'data/processed/visualization_data/predicted'

shutil.copy(background_path, dst_path)
shutil.copy(recording_meat_path, dst_path)
shutil.copy(background_path, dst_path_pred)
shutil.copy(recording_meat_path, dst_path_pred)
shutil.copy(tracks_meta_file, dst_path_pred)

# Get columns from the newly created dataset
def get_columns(file_dir):
    print(file_dir)
    df = pd.read_csv(file_dir)

    # get the columns
    s_x = df['xCenter'].values
    s_y = df['yCenter'].values
    v_x = df['xVelocity'].values
    v_y = df['yVelocity'].values
    a_x = df['xAcceleration'].values
    a_y = df['yAcceleration'].values

    return s_x , s_y , v_x , v_y , a_x , a_y
s_x, s_y, v_x, v_y, a_x, a_y = get_columns(track_vis_path)
