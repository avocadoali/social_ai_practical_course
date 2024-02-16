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
