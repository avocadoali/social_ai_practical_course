# Social AI

This repository contains the code for the practical course: Motion Planing of Autnomous Vehicles - Social AI 

We are looking for an algorithm which implements the social interaction between cars. 
For that we have to find a way to describe the motion of each car first. 
The goal is to find an efficient and accurate numerical integration model. 

## Project Structure


The project is structured as follows:
```
├── config
├── data
│   ├── processed
│   └── raw
├── notebooks
├── reports
├── results
│   └── models
└── src
    ├── data_processing
    ├── integration_method
    ├── modeling
    └── utils

```

Here's a brief overview of the directory structure:

- **config:** Contains the configuration file for all project settings.

- **data:**
  - **raw:** Holds the raw, unprocessed data.
  - **processed:** Stores the processed data generated during the data processing phase.

- **notebooks:** This directory contains Jupyter notebooks used for testing and exploring the dataset.

- **reports:** Used for project reports and formulas used in the project.

- **results:**
  - **models:** Saves trained models 

- **src:**
  - **data_processing:** Houses scripts/modules for data preprocessing.
  - **modeling:** Contains the code for our linear model
  - **utils:** Holds utility functions and helper modules such as columns imports and a linear regression module.

## Running the project

Create the python environment (we are using conda for the environment and pip to install the requirement. Feel free to use whatever setup works best for you):

```bash
conda create -n your_env_name
```

Activate the environment:

```bash
conda activate your_env_name
```

Install the requirements:
```bash
pip install -r requirements.txt
```


Put the exiD, rounD, and inD datasets into the data/raw path.

```bash
cp -r <path_to>/exiD <path_to_root_of_project>/data/raw
cp -r <path_toby>/inD <path_to_root_of_project>/data/raw
cp -r <path_toby>/rounD <path_to_root_of_project>/data/raw
```


Then, run the data_processing_all.py script from the root of this project:

```python 
python src/data_processing/data_processing_all.py 
```
This will perform the data processing for training all the models (this can take a while).

Now you are able to run all the Jupyter Notebooks in the modeling and integration_method directory.
The most interesting are the linear_model.ipynb and the ballistic_integration.ipynb
```
run linear_model.ipynb and ballistic_integration.ipynb through your prefered IDE
```

You can also just run the main.py to both run the preprocessing and the training and evaluation of our linear model.
Though, I really encourage you to run the notebook for a better visual understanding.

```python 
python main.py
```

## Visualization of the linear model
To run the visualization of a prediction run the visualization_data.py

```python
python src/data_processing/visualsation_data.py 
```

You can specify what you want to visualize in the config.yaml at the visulation part.
This will run its own preprocessing and predict the selected dataset.
For more seamless use, I suggest you to set the show_and_save_figure in the config file to false.
``` yaml
  show_and_save_figures: False
```

The dataset which you can find in the 'base_processed_path', which
was set in the config file, will contain a predicted and ground_truth directory. 
In there, you can find the dataset which can be visualized using the drone-dataset-tool. 
For further instructions on how to use that tool visit their github repo [here](https://github.com/ika-rwth-aachen/drone-dataset-tools) and substitute their data directory with either the ground_truth or predicted directory.
Here is an example (note that we are now in the drone-dataset-tools repo):

For the ground truth
```bash
   python3 run_track_visualization.py --dataset_dir <path_to_root_of_project>/data/processed/visualization_data/ground_truth --dataset ind --recording 00
```

For our predicted data
```bash
   python3 run_track_visualization.py --dataset_dir <path_to_root_of_project>/data/processed/visualization_data/predicted --dataset ind --recording 00
```

