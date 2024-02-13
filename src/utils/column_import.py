import pandas as pd
import os

from src.utils.load_config import load_config


def import_columns(file_dir):
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

def import_columns_dif(file_dir):
    print(file_dir)
    df = pd.read_csv(file_dir)

    # get the columns
    s_x = df['xCenter'].values
    s_y = df['yCenter'].values
    v_x = df['xVelocity'].values
    v_y = df['yVelocity'].values
    a_x = df['xAcceleration'].values
    a_y = df['yAcceleration'].values
    a_x_a = df['xAcceleration_a']
    a_y_a = df['yAcceleration_a']
    a_x_b = df['xAcceleration_b']
    a_y_b = df['yAcceleration_b']
    v_x_a = df['xVelocity_a']
    v_y_a = df['yVelocity_a']
    v_x_b = df['xVelocity_b']
    v_y_b = df['yVelocity_b']
    s_x_a = df['xCenter_a']
    s_y_a = df['yCenter_a']
    s_x_b = df['xCenter_b']
    s_y_b = df['yCenter_b']

    return s_x , s_y , v_x , v_y , a_x , a_y, a_x_a , a_y_a , a_x_b , a_y_b 

def main():
    config = load_config()['data']['processed_data_path_ind_test_set']

    processed_data_test_set_0 = config['processed_data_test_set_0']
    processed_data_dif_set = config['processed_data_dif_set']

    #create directory if not exists
    if not os.path.exists(processed_data_dif_set):
        os.makedirs(processed_data_dif_set)

    if not os.path.exists(processed_data_test_set_0):
        os.makedirs(processed_data_test_set_0)


    # Import test set 0
    columns = import_columns(processed_data_test_set_0)
    #columns_dif = import_columns_dif(processed_data_dif_set)
    print('printing columns:')
    print(columns)
    return columns


columns = main()
    
