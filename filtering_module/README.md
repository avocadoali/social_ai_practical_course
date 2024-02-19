# Filtering Module

## Introduction

The Filtering Module is a comprehensive solution designed to process and analyze vehicle interaction data. It offers a variety of filters for different interactions, utilities for data manipulation, and a main script for executing the core logic.

## Structure Overview

### Root Directory:

- `tracks.csv`: A CSV file containing track data.
- `requirements.txt`: Lists all Python package dependencies for the module.
- `README.md`: Documentation for the module, providing an overview and instructions.
- `main.py`: The main Python script for executing the module's functionality.
- `data.txt`: A text file containing additional data used by the module.

### Directories:

- `interactions_filter/`: Contains Python scripts for different interaction filters, such as `overtaking.py`, `lane_changing.py`, etc. Also includes a `__pycache__` directory for compiled Python files.
- `csv_files/`: Contains CSV files with data for other and current cars, distinguished by specific IDs and general datasets.
- `utilities/`: Includes utility scripts like `data_loading.py` and `track_import.py`, along with a `__pycache__` directory for compiled files.
- `data/`: Contains directories named `inD`, `exid`, and `round`, each with its own set of data files including CSV files for recording metadata, background images, track data, and tracks metadata.

## Installation

To set up the Filtering Module, start by installing the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Ensure you have Python 3.8 or above installed.
2. Place your datasets in the project root or specify the path when calling data loading functions.
3. Run `main.py` to execute the program.

```bash
python main.py
```

# Analyzing Vehicles

This program analyzes vehicles in the dataset. It processes every car in order, and the progress is displayed on the console.
The analysis starts with the following indicator: "------------ Analyzing vehicles ------------".

1. When the program encounters micro behaviors such as hard braking, lane changes, overtaking, etc., it will indicate them in the console in the following format:
"Hard braking detected for Track ID {trackId} in frames {frame_range}"


2. There are further indicators which are commented out. They are described in the code. You just need to delete the comment sign in front of it. For example:

    ```python
    # print(f"Vehicles {current_trackId} and {trackId} are close (distance: {distance}) at frame {frame}")
    ```
    Just delete the comment sign and the program will display the message in the console.
    ```python
    print(f"Vehicles {current_trackId} and {trackId} are close (distance: {distance}) at frame {frame}")
    ```

3. When analyzing the vehicles, the program will output the cars which are getting close like this example (for each car and at the each step):
    ```
    {(4, 5): [(83, 4, 5, 0, 43.2162538456308, 44.2351, -3.4165, 43.7038, -5.5957, 0.4539, 1.467, 0.4935, 1.5686, 401.9079, -213.1897, 358.9013, -208.938)]}
    ```
    The output follows this structure:
    ```
    [First car Id, Second car Id): [Recording Id, First Car Id, Second Car Id, Frame number, distance between cars, First car Velocity, First car yVelocity, Second car xVelocity, Second car yVelocity, First car Acceleration, First car Acceleration, Second car Acceleration, Second car Acceleration)]}, {({...): [(..)]}
    ```
    At the end of the program, the output will be transformed (for each car) into a CSV file and saved in the "csv_files" directory. It can be later used for the integration module. For each recording, the file will be label with the recording id.


4. Vehicles which are changing lanes are also indicated in the console.


5. In the latest output of the program, you will see the following:
"---record entering exiting---" indicator, which outputs the entering and exiting behavior in this format:
    ```
    (recording id, current track id, x, frame number, x, entering or exiting behavior)
    ```
   
6. After the indicator, "These are the cars getting closer and having interaction," all interacting cars in the current recording are outputted in this structure:
    ```
    {[First car Id, Second car Id): [Recording Id, First Car Id, Second Car Id, Frame number, distance between cars, First car Velocity, First car yVelocity, Second car xVelocity, Second car yVelocity, First car Acceleration, First car Acceleration, Second car Acceleration,
    Second car Acceleration)]}, {({...): [(..)]}
    ```
