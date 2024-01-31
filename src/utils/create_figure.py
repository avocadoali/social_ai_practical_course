import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def evaluate_and_save(y_test, y_pred, save_path, title):
    
    # Evaluate the model using various metrics
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Print the results in scientific notation
    print(f'Mean Squared Error (MSE): {mse:.4e}')
    print(f'Mean Absolute Error (MAE): {mae:.4e}')
    print(f'R-squared (R²) Score: {r2:.4e}')

    # Create a scatter plot
    plt.scatter(y_test, y_pred, alpha=0.7)

    # Add a diagonal line for reference (perfect prediction)
    min_val = min(np.min(y_test), np.min(y_pred))
    max_val = max(np.max(y_test), np.max(y_pred))
    plt.plot([min_val, max_val], [min_val, max_val], linestyle='--', color='red', linewidth=2, label='Perfect Prediction')

    # Add labels and title
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title(title)

    # Set aspect ratio to be equal
    plt.gca().set_aspect('equal', adjustable='box')

    # Show legend
    plt.legend()

    plt.gcf().set_size_inches(7,7)  # Adjust the size as needed
    plt.savefig(save_path)


    # Show the plot
    plt.show()
