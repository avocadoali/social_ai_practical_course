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

- **config:** Contains configuration files for various project settings.

- **data:**
  - **raw:** Holds the raw, unprocessed data.
  - **processed:** Stores the processed data generated during the data processing phase.

- **notebooks:** This directory contains Jupyter notebooks used for testing and exploring the dataset.

- **reports:** Used for project reports and formulas used in the project.

- **results:**
  - **models:** Saves trained models 

- **src:**
  - **data_processing:** Houses scripts/modules for data preprocessing.
  - **integration_method:** Includes the code for the integration methods
  - **modeling:** Contains the code for building and training the models.
  - **utils:** Holds utility functions and helper modules such as colums imports and a linear regression module.


## Running the porject

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

Now you are able to run all the Jupyter Notebooks in the modeling and integration_method directory.

To visualize the findings run the 