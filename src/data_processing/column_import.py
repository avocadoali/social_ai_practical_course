import pandas as pd

# Specify the paths and track id
dataset_dir = '../../data/processed/x_y_recording00_range382'
#dataset_dir = '../../data/processed/x_y_recording00_range1'

# Use pandas to read the CSV file into a DataFrame
df = pd.read_csv(dataset_dir)

# get the columns
s_x = df['xCenter'].values
s_y = df['yCenter'].values
v_x = df['xVelocity'].values
v_y = df['yVelocity'].values
a_x = df['xAcceleration'].values
a_y = df['yAcceleration'].values

