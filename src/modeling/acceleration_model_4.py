# Imports
import numpy as np
from src.utils.evaluate import evaluate
from src.utils.linear_regressor import perform_linear_regression
from src.utils.column_import import columns


def run_model(columns):

    # Extracting individual columns from the dataset
    s_x, s_y, v_x, v_y, a_x, a_y = columns

    # Target vector y
    y = np.concatenate([a_x[0:-2], a_y[0:-2]])    # a(k)
    y.shape

    # Input features X_first_model of the first model
    A = - a_x[1:-1]                
    B = - a_y[1:-1]                
    C = v_x[2:] - v_x[1:-1]        
    D = v_y[2:] - v_y[1:-1]        

    X_first_model = np.vstack((
        np.column_stack((A, C)),
        np.column_stack((B, D))
    ))

    X_first_model.shape

    # First model
    first_model = perform_linear_regression(X_first_model, y)

    # Input features X_second_model of the second model
    dt = 0.04

    A = - a_x[1:-1]                                 
    B = - a_y[1:-1]                                 

    # Using position and velocity data for the second model
    C = s_x[2:] - s_x[1:-1] - dt * v_x[1:-1]        
    D = s_y[2:] - s_y[1:-1] - dt * v_y[1:-1]        

    X_second_model = np.vstack((
        np.column_stack((A, C)), 
        np.column_stack((B, D))
    ))

    print(X_second_model.shape)

    # Second model
    second_model = perform_linear_regression(X_second_model, y)

    # Extracting coefficients from the models
    c_1_overline = first_model.coef_[0]
    c_2_overline = first_model.coef_[1]
    c_3_overline = second_model.coef_[0]
    c_4_overline = second_model.coef_[1]

    # Calculating inverse coefficients for later use
    c_2 = 1 / c_2_overline
    c_1 = c_1_overline * c_2
    c_4 = 1 / c_4_overline
    c_3 = c_3_overline * c_4

    # Extracting different time steps and variables
    s_x_0 = s_x[:-2]
    s_y_0 = s_y[:-2]
    s_x_1 = s_x[1:-1]
    s_y_1 = s_y[1:-1]
    s_x_2 = s_x[2:]
    s_y_2 = s_y[2:]
    v_x_1 = v_x[1:-1]
    v_y_1 = v_y[1:-1]
    v_x_2 = v_x[2:]
    v_y_2 = v_y[2:]
    a_x_1 = a_x[1:-1]
    a_y_1 = a_y[1:-1]
    a_x_0 = a_x[:-2]
    a_y_0 = a_y[:-2]

    # Prediction using the first model
    a_xy_0_pred_first_model = first_model.predict(X_first_model)

    # Splitting the predictions for x and y components
    half = int(len(a_xy_0_pred_first_model) / 2)
    a_x_0_pred = a_xy_0_pred_first_model[:half]
    a_y_0_pred = a_xy_0_pred_first_model[half:]

    # Predicting velocity for the next time step
    v_x_2_pred = c_2 * a_x_0_pred + c_1 * a_x_1 + v_x_1
    v_y_2_pred = c_2 * a_y_0_pred + c_1 * a_y_1 + v_y_1

    # Evaluating the predictions
    evaluate(v_x_2, v_x_2_pred)
    evaluate(v_y_2, v_y_2_pred)

    # Prediction using the second model
    a_xy_0_pred_second_model = second_model.predict(X_second_model)

    # Splitting the predictions for x and y components
    half = int(len(a_xy_0_pred_second_model) / 2)
    a_x_0_pred = a_xy_0_pred_second_model[:half]
    a_y_0_pred = a_xy_0_pred_second_model[half:]

    # Predicting position for the next time step
    s_x_2_pred = s_x_1 + dt * v_x_1 + c_3 * a_x_1 + c_4 * a_x_0_pred
    s_y_2_pred = s_y_1 + dt * v_y_1 + c_3 * a_y_1 + c_4 * a_y_0_pred

    # Evaluating the predictions
    evaluate(s_x_2, s_x_2_pred)
    evaluate(s_y_2, s_y_2_pred)


if __name__ == '__main__':
    run_model(columns)