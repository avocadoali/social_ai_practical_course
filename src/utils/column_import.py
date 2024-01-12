import pandas as pd
import os

from config.settings import processed_data_test_set_0


def import_columns(file_dir):
    # Use pandas to read the CSV file into a DataFrame
    # Check if the file exists
    if not os.path.exists(file_dir):
        print('File does not exist')
        return 0
        

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

# Import test set 0
columns = import_columns(processed_data_test_set_0)

