import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import Ridge
from src.utils.evaluate_and_save import evaluate_and_save

def perform_linear_regression(X, y, title):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)



    alpha = 1.0  # regularization strength
    #model = LinearRegression()
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    ## Train a linear regression model
    #model = LinearRegression()
    #model.fit(X_train, y_train)

    ## Make predictions on the test set
    #y_pred = model.predict(X_test)

    # Evaluate the model using various metrics
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Print the results in scientific notation
    ### TODO print(f'Mean Squared Error (MSE): {mse:.4e}')
    ### TODO print(f'Mean Absolute Error (MAE): {mae:.4e}')
    ### TODO print(f'R-squared (R²) Score: {r2:.4e}')

    ### Coefficients
    ## TODO print('Coefficients:')
    ## TODO for x in model.coef_:
    ## TODO     print(x)

    evaluate_and_save(y_test, y_pred, title, 'Actual Acceleration Values', 'Predicted Acceleration Value')

    return model