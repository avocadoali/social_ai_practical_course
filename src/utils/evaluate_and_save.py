import matplotlib.pyplot as plt
import numpy as np
import yaml
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


SMALL_SIZE = 15
MEDIUM_SIZE = 17
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title



def load_config():
    with open('config/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)['figures']

    return config

def evaluate_and_save(y_test, y_pred, title, xlabel = 'Actual Values', ylabel = 'Predicted Values', set_limit = False):
 

    show_figure = load_config()['show_and_save_figures']
    save_path = load_config()['figures_save_path']
    
    # Evaluate the model using various metrics
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Print the results in scientific notation
    print(f'Mean Squared Error (MSE): {mse:.4e}')
    print(f'Mean Absolute Error (MAE): {mae:.4e}')
    print(f'R-squared (R²) Score: {r2:.4e}')

    if show_figure:
        # Create a scatter plot
        plt.scatter(y_test, y_pred, alpha=0.7)

        if set_limit:
            # Setting limits for x and y axes
            plt.xlim(-6, 6)
            plt.ylim(-6, 6)

        # Add a diagonal line for reference (perfect prediction)
        min_val = min(np.min(y_test), np.min(y_pred))
        max_val = max(np.max(y_test), np.max(y_pred))
        plt.plot([min_val, max_val], [min_val, max_val], linestyle='--', color='red', linewidth=2, label='Perfect Prediction')

        # Add labels and title
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

        # Set aspect ratio to be equal
        plt.gca().set_aspect('equal', adjustable='box')

        # Show legend
        plt.legend()

        plt.gcf().set_size_inches(7,7)  # Adjust the size as needed
        plt.savefig( os.path.join(save_path, title + '.png'))


        # Show the plot
        plt.show()

def residuals_plot(values_ground_truth, values_pred, title):
    # Calculate residuals
    residuals = np.array(values_ground_truth) - np.array(values_pred)

    # Plot residuals
    plt.figure(figsize=(8, 6))
    plt.scatter(values_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title(title)
    plt.grid(True)
    plt.show()

