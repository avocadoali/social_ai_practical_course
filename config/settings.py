import os

## Root directory
ROOT_DIR = "/home/ali/tum/motion_planning/social_ai_practical_course"


# Access paths
# Make dataset path
def data_path(path):
    return os.path.abspath(os.path.join(ROOT_DIR, path))

raw_data_path_ind =         data_path("data/raw/inD/data/")
processed_data_test_set_0 = data_path("data/processed/x_y_recording_00_range_384.csv")
saved_models_path =           data_path("results/models/")