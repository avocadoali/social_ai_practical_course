import matplotlib.pyplot as plt

from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def perform_linear_regression(A, t):
    X_train, X_test, y_train, y_test = train_test_split(A, t, test_size=0.2, random_state=69)

    ### Fitting
    model = LinearRegression()
    model.fit(X_train, y_train)

    ### Coefficients
    print('Coefficients:')
    for x in model.coef_:
        print(x)

    ### Evaluation
    #### MSE
    # Use the model to predict on the test set
    predictions = model.predict(X_test)

    # Evaluate the performance
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse}')

    #### R-score
    # Calculate R-squared
    r2 = r2_score(y_test, predictions)
    print("R-squared (R2) Score:", r2)

    #### Residual plot
    # Calculate residuals
    residuals = y_test - predictions

    # Create a scatter plot of predicted vs actual values
    plt.scatter(predictions, residuals, alpha=0.5)
    plt.title('Residuals Plot')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.axhline(y=0, color='black', linestyle='--', linewidth=2)  # Add a horizontal line at y=0
    plt.show()

    # Plotting Predicted vs. Actual
    plt.scatter(y_test, predictions)
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', linewidth=2)  # Diagonal line
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.title("Predicted vs. Actual Plot")