# Acceleration model 4 parameters (Best one)
'''
I know this is cursed but I just converted the notebook so we can run it as a pyhon script.
Have a look into the notebook in the notebooks directory for a better visual understanding. 
'''

## Imports
import numpy as np
from src.utils.evaluate_and_save import evaluate_and_save
from src.utils.linear_regressor import perform_linear_regression
from src.utils.column_import import columns

"""
Here we extract the needed column for the training and prediciton.

Note that we have to do some shifting index shifting.
For example for the acceleration colum it looks like this:

| a(k-1) | a(k)    | a(k+1) |
|--------|---------|--------|
| a[:-2] | a[1:-1] | a[2:]  |

"""


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

## Training our linear model
"""
We want to solve our Distance Model:

\begin{align} 
    \begin{bmatrix}
        a_x(k) \\ 
        a_y(k)       
    \end{bmatrix}_{\text{dis}}
    =
    \begin{bmatrix}
       s_x(k) - s_x(k+1) - v_x(k) & -a_x(k-1) \\ 
       s_y(k) - s_y(k+1) - v_y(k) & -a_y(k-1)   
    \end{bmatrix}
    \begin{bmatrix}
        \overline{c}_1 \\
        \overline{c}_2 \\
   \end{bmatrix}
\end{align}

The accleration vector on the left will be our target vector 'y' and the right side of the model is the matrix 'X_distance_model'
"""


# Target vector 
y = np.concatenate([a_x_1, a_y_1])  
y.shape

# matrix distance model
A = s_x_2 - s_x_1 - v_x_1        
B = s_y_2 - s_y_1 - v_y_1        
C = - a_x_0                                 
D = - a_y_0                                 

X_distance_model = np.vstack((
    np.column_stack((A, C)), 
    np.column_stack((B, D))
))


"""
Similarly we define the matrix on the right hand side of the equation of the velocity model:

\begin{align} 
    \begin{bmatrix}
        a_x(k) \\ 
        a_y(k) 
    \end{bmatrix}_{\text{vel}}
    =
    \begin{bmatrix}
        v_x(k) - v_x(k+1) & -a_x(k+1)    \\ 
        v_y(k) - v_y(k+1) & -a_y(k+1)    \\
    \end{bmatrix}
    \begin{bmatrix}
        \overline{c}_3 \\
        \overline{c}_4 \\
   \end{bmatrix}
\end{align}


Note that the acceleration vector on the left is the same as above. This is done specifically so our models are trained such that both models have the same acceleration output!
"""

# matrix velocity model
A = v_x_2 - v_x_1        
B = v_y_2 - v_y_1        
C = - a_x_0
D = - a_y_0

X_velocity_model = np.vstack((
    np.column_stack((A, C)),
    np.column_stack((B, D))
))

"""
Now we can train our models and evaluate them on a test set that we create. 

Have a look into the perform_linear_regression() function
"""

# Train both models
velocity_model = perform_linear_regression(X_velocity_model, y, 'Prediction Acceleration (Linear Model, Velocity)')

distance_model = perform_linear_regression(X_distance_model, y, 'Prediction Acceleration (Linear Model, Distance)')

"""
Now we can see test how the model perform in their prediction
"""

# Predict the acceleration for both models
y_pred_distance_model =  distance_model.predict(X_distance_model)
y_pred_velocity_model =  velocity_model.predict(X_velocity_model)

"""
Here we test how equal their results are
"""

# Evaluate the equvialence of the predicted accelerations
evaluate_and_save( y_pred_distance_model, y_pred_velocity_model, 'Acceleration Equivalence (Linear Model)', 'Acceleration (Distance Formula)', 'Acceleration (Velocity Formula)')

## Rearrange the models

"""
Now we rearrange our model such that the distance and velocity are on the left:

\begin{align} 
    s(k+1) &= s(k) + v(k) + c_1 a_{dis}(k) + c_2 a(k-1) \\
    v(k+1) &= v(k)        + c_3 a_{vel}(k) + c_4 a(k-1)
\end{align}

To solve this we have to recalculate the coefficients we got from our training:

\begin{align}
   c_1 &= \frac{1}{\bar{c}_1} \\
   c_2 &= \bar{c}_2 \cdot c_1 \\
   c_3 &= \frac{1}{\bar{c}_3} \\
   c_4 &= \bar{c}_4 \cdot c_3
\end{align}

This is done in the following:
"""

# Extracting coefficients from the models
c_1_overline = distance_model.coef_[0]
c_2_overline = distance_model.coef_[1]
c_3_overline = velocity_model.coef_[0]
c_4_overline = velocity_model.coef_[1]

# Recalculate them
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

# Prediction using the velocity model
a_xy_1_pred_velocity_model = velocity_model.predict(X_velocity_model)

# Splitting the predictions for x and y components
half = int(len(a_xy_1_pred_velocity_model) / 2)
a_x_1_pred_vel = a_xy_1_pred_velocity_model[:half]
a_y_1_pred_vel = a_xy_1_pred_velocity_model[half:]


"""
Now we can put everything into our distance formula. In matrix form it looks like this:

\begin{align}
    \begin{bmatrix} s_x(k+1) \\ s_y(k+1) \end{bmatrix}
    =
    \begin{bmatrix} a_x(k) & a_x(k-1)    \\ a_y(k) & a_y(k-1)    \\ \end{bmatrix}
    \begin{bmatrix} c_1 \\ c_2 \\ \end{bmatrix}
    +
    \begin{bmatrix} s_x(k) + v_x(k) \\ s_y(k) + v_y(k) \\ \end{bmatrix}
\end{align} 
"""


# Distance formula 
s_x_2_pred = s_x_1 + v_x_1 + c_1 * a_x_1_pred_dist + c_2 * a_x_0
s_y_2_pred = s_y_1 + v_y_1 + c_1 * a_y_1_pred_dist + c_2 * a_y_0

# Concate results for easier usage later
s_xy_2 = np.concatenate((s_x_2, s_y_2))
s_xy_2_pred = np.concatenate((s_x_2_pred, s_y_2_pred))


# Distance formula 
s_x_2_pred = s_x_1 + v_x_1 + c_1 * a_x_1_pred_dist + c_2 * a_x_0
s_y_2_pred = s_y_1 + v_y_1 + c_1 * a_y_1_pred_dist + c_2 * a_y_0

# Concate results for easier usage later
s_xy_2 = np.concatenate((s_x_2, s_y_2))
s_xy_2_pred = np.concatenate((s_x_2_pred, s_y_2_pred))

# Predicting velocity for the next time step
v_x_2_pred = v_x_1 + c_3 * a_x_1_pred_vel + c_4 * a_x_0
v_y_2_pred = v_y_1 + c_3 * a_y_1_pred_vel + c_4 * a_y_0

# Concate results for easier usage later
v_xy_2 = np.concatenate((v_x_2, v_y_2))
v_xy_2_pred = np.concatenate((v_x_2_pred, v_y_2_pred))



"""
Now we can evalute our results# Predicting velocity for the next time step
"""

v_x_2_pred = v_x_1 + c_3 * a_x_1_pred_vel + c_4 * a_x_0
v_y_2_pred = v_y_1 + c_3 * a_y_1_pred_vel + c_4 * a_y_0

# Concate results for easier usage later
v_xy_2 = np.concatenate((v_x_2, v_y_2))
v_xy_2_pred = np.concatenate((v_x_2_pred, v_y_2_pred))


# Evaluating the predictions
evaluate_and_save(s_xy_2, s_xy_2_pred, 'Prediction Distance using the coefficients', xlabel='Distance ground truth', ylabel='Distance predicted')
evaluate_and_save(v_xy_2, v_xy_2_pred, 'Prediction Velocity using the coefficients', xlabel='Velocity ground truth', ylabel='Velocity predicted')


# Distance formula 
s_x_2_pred = s_x_1 + v_x_1 + c_1 * a_x_1_pred_dist + c_2 * a_x_0
s_y_2_pred = s_y_1 + v_y_1 + c_1 * a_y_1_pred_dist + c_2 * a_y_0

# Concate results for easier usage later
s_xy_2 = np.concatenate((s_x_2, s_y_2))
s_xy_2_pred = np.concatenate((s_x_2_pred, s_y_2_pred))






