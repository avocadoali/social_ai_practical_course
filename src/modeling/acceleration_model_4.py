# Imports
import numpy as np
from src.utils.evaluate_and_save import evaluate_and_save
from src.utils.linear_regressor import perform_linear_regression
from src.utils.column_import import columns


# Extracting individual columns from the dataset
s_x, s_y, v_x, v_y, a_x, a_y = columns
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

a_x_0 = a_x[:-2]
a_y_0 = a_y[:-2]
a_x_1 = a_x[1:-1]
a_y_1 = a_y[1:-1]

# Create the models (y, X_velocity_model, X_distance_model)
# Target vector y
y = np.concatenate([a_x_1, a_y_1])  
y.shape
 
# distance model X_distance_model
dt = 0.04
A = s_x_2 - s_x_1 - v_x_1        
B = s_y_2 - s_y_1 - v_y_1        
C = - a_x_0                                 
D = - a_y_0                                 
X_distance_model = np.vstack((
    np.column_stack((A, C)), 
    np.column_stack((B, D))
))

# velocity model X_velocity_model
A = v_x_2 - v_x_1        
B = v_y_2 - v_y_1        
C = - a_x_0
D = - a_y_0
X_velocity_model = np.vstack((
    np.column_stack((A, C)),
    np.column_stack((B, D))
))

# Train both models
velocity_model = perform_linear_regression(X_velocity_model, y, 'Prediction Acceleration (Linear Model, Velocity)')
distance_model = perform_linear_regression(X_distance_model, y, 'Prediction Acceleration (Linear Model, Distance)')

# Predict the acceleration for both models
y_pred_distance_model =  distance_model.predict(X_distance_model)
y_pred_velocity_model =  velocity_model.predict(X_velocity_model)

# Evaluate the equvialence of the predicted accelerations
evaluate_and_save( y_pred_distance_model, y_pred_velocity_model, 'Acceleration Equivalence (Linear Model)', 'Acceleration (Distance Formula)', 'Acceleration (Velocity Formula)')

# Rearange the models for distance and velocity
# Extracting coefficients from the models
c_1_overline = distance_model.coef_[0]
c_2_overline = distance_model.coef_[1]
c_3_overline = velocity_model.coef_[0]
c_4_overline = velocity_model.coef_[1]
c_1 = 1 / c_1_overline
c_2 = c_2_overline * c_1
c_3 = 1 / c_3_overline
c_4 = c_4_overline * c_3

# Prediction using the distance model
a_xy_1_pred_distance_model = distance_model.predict(X_distance_model)

# Splitting the predictions for x and y components
half = int(len(a_xy_1_pred_distance_model) / 2)
a_x_1_pred_dist = a_xy_1_pred_distance_model[:half]
a_y_1_pred_dist = a_xy_1_pred_distance_model[half:]

# Predicting velocity for the next time step
s_x_2_pred = s_x_1 + v_x_1 + c_1 * a_x_1_pred_dist + c_2 * a_x_0
s_y_2_pred = s_y_1 + v_y_1 + c_1 * a_y_1_pred_dist + c_2 * a_y_0

# Concate results
s_xy_2 = np.concatenate((s_x_2, s_y_2))
s_xy_2_pred = np.concatenate((s_x_2_pred, s_y_2_pred))

# Prediction using the velocity model
a_xy_1_pred_velocity_model = velocity_model.predict(X_velocity_model)

# Splitting the predictions for x and y components
half = int(len(a_xy_1_pred_velocity_model) / 2)
a_x_1_pred = a_xy_1_pred_velocity_model[:half]
a_y_1_pred = a_xy_1_pred_velocity_model[half:]

# Predicting velocity for the next time step
v_x_2_pred = v_x_1 + c_3 * a_x_1_pred + c_4 * a_x_0
v_y_2_pred = v_y_1 + c_3 * a_y_1_pred + c_4 * a_y_0

# Concate results
v_xy_2 = np.concatenate((v_x_2, v_y_2))
v_xy_2_pred = np.concatenate((v_x_2_pred, v_y_2_pred))

# Evaluating the predictions
evaluate_and_save(s_xy_2, s_xy_2_pred, 'Prediction Distance using the coefficients', xlabel='Distance ground truth', ylabel='Distance predicted')
evaluate_and_save(v_xy_2, v_xy_2_pred, 'Prediction Velocity using the coefficients', xlabel='Velocity ground truth', ylabel='Velocity predicted')
