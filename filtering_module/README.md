## Project Structure

The project is organized into different directories for better modularity and ease of understanding:

- **interactions_filter**: Contains the filtering logic for different types of interactions.
- **utilities**: Contains general utility functions including data loading functions.
- **main.py**: The main script to run the project.

### Directory: interactions_filter

- **`__init__.py`**: Initializes the interactions_filter package.
- **exiting_behaviour.py**: Contains the logic for filtering exiting behavior interactions.
- **merge_onto_exit_ramps.py**: Contains the logic for filtering merging onto exit ramps interactions.
- **yielding_behaviour.py**: Contains the logic for filtering yielding behavior interactions.
- **speed_adjustment.py**: Contains the logic for filtering speed adjustment interactions.
- **merging_and_lane_changing.py**: Contains the logic for filtering merging and lane changing interactions.

### Directory: utilities

- **`__init__.py`**: Initializes the utilities package.
- **data_loading.py**: Contains functions to load datasets.
- **track_import.py**: Imports the tracks from the datasets.

## Usage

1. Ensure you have Python 3.8 or above installed.
2. Place your datasets in the project root or specify the path when calling data loading functions.
3. Run `main.py` to execute the program.

```bash
python main.py
