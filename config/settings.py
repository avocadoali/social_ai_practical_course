import os

## Root directory
ROOT_DIR = "/home/ali/tum/motion_planning/social_ai_practical_course"


# Access paths
# Make dataset path
def data_path(path):
    return os.path.abspath(os.path.join(ROOT_DIR, path))

raw_data_path_ind = data_path("data/raw/inD/data/")
raw_data_path_exid= data_path("data/raw/exiD/data/")
processed_data_inD = data_path("data/processed/inD/")
processed_data_exiD = data_path("data/processed/exiD/")

processed_data_dif_set = data_path('data/processed/scenario_samples/test_set/lane_merging_merged_dif_test.csv')
processed_data_dif_set = data_path('data/processed/scenario_samples/lane_merging/dif_set/test_set_00.csv')

processed_data_test_set_0 = data_path("data/processed/inD/x_y_recording_00_range_384.csv")
saved_models_path = data_path("results/models/")

delta_model_path = data_path("delta_model_model_2/.pt")
