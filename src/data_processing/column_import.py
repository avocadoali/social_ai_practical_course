import pandas as pd
from .config_file import dataset_dir

# Use pandas to read the CSV file into a DataFrame
print('Importet column directory')
print(dataset_dir)
df = pd.read_csv(dataset_dir)


# get the columns
s_x = df['xCenter'].values
s_y = df['yCenter'].values
v_x = df['xVelocity'].values
v_y = df['yVelocity'].values
a_x = df['xAcceleration'].values
a_y = df['yAcceleration'].values

