# This file configures all paths to the datasets

# For data_import.py
# Dataset directory and number of the recording
import os
from definitions import ROOT_DIR

dataset_dir_raw = '../../data/raw/inD/data/'
recording = "00"

# Number of tracks to include
n = 384

# For column import 
dataset_file = f'data/processed/x_y_recording_{recording}_range_{n}.csv'
dataset_dir = os.path.join(ROOT_DIR, dataset_file)