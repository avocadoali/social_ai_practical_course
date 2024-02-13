import pandas as pd
import shutil
import os
import yaml
from src.modeling.linear_model import predicted_columns

# Read the YAML configuration file
with open('config/config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)['visualisation']
    

# Store variables accordingly
base_raw_path = config['base_raw_path']
base_processed_path = config['base_processed_path']
tracks_number = config['tracks_number']
tracks_meta_number = config['tracks_meta_number']
recording_meat_number = config['recording_meat_number']
background_number = config['background_number']
track_ids = config['track_ids']

# Define specific paths
raw_track_path = os.path.join(base_raw_path, tracks_number)
background_path = os.path.join(base_raw_path, background_number)
recording_meta_path = os.path.join(base_raw_path, recording_meat_number)
ground_truth_path = os.path.join(base_processed_path, 'ground_truth/')
predicted_path = os.path.join(base_processed_path, 'predicted')

os.makedirs(base_processed_path, exist_ok=True)
os.makedirs(ground_truth_path, exist_ok=True)
os.makedirs(predicted_path, exist_ok=True)

# Read raw track data and filter by track ID
df = pd.read_csv(raw_track_path, low_memory=False)

track_one_car = df[df['trackId'].isin(track_ids)]

# Define paths for ground truth data
tracks_ground_truth_path = os.path.join(ground_truth_path, tracks_number)
tracks_meta_ground_truth_path = os.path.join(ground_truth_path, tracks_meta_number)

# Save filtered track data and corresponding metadata
track_one_car.to_csv(tracks_ground_truth_path, index=False)


tracks_meta = pd.read_csv(os.path.join(base_raw_path, tracks_meta_number))

tracks_meta_one_car = pd.DataFrame()
if len(track_ids) > 0:
    tracks_meta_one_car = tracks_meta[tracks_meta['trackId'].isin(track_ids)]

tracks_meta_one_car.to_csv(tracks_meta_ground_truth_path, index=False)

# Copy background and recording meta to ground truth and predicted paths
for path in [background_path, recording_meta_path]:
    shutil.copy(path, ground_truth_path)
    shutil.copy(path, predicted_path)

# Copy tracks metadata from ground truth to predicted path
shutil.copy(tracks_meta_ground_truth_path, os.path.join(predicted_path, tracks_meta_number))

# Get the needed columns for the predicition

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

columns = get_columns(tracks_ground_truth_path)

# Predict the dataset
result = predicted_columns(columns)
df = pd.read_csv(tracks_ground_truth_path)
df_new = df.iloc[:-2].copy()
df_new['xCenter']   = result['s_x'].tolist()
df_new['yCenter']   = result['s_y'].tolist()
df_new['xVelocity'] = result['v_x'].tolist()
df_new['yVelocity'] = result['v_y'].tolist()
df_new['xAcceleration'] = result['a_x'].tolist()
df_new['yAcceleration'] = result['a_y'].tolist()


dst_path_df = os.path.join(predicted_path, tracks_number )
df_new.to_csv(dst_path_df,  index=False)
print(f'Save to: {dst_path_df}')

