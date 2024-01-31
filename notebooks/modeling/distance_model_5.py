# Import libraries and data
import os
import numpy as np
import pickle


from config.settings import ROOT_DIR, saved_models_path
from src.utils.linear_regressor import perform_linear_regression
from src.utils.column_import import columns
s_x, s_y, v_x, v_y, a_x, a_y = columns

X_x= np.vstack((
    s_x[2:-1],        #s[k]   
    s_x[1:-2],        #s[k-1]
    s_x[ :-3],        #s[k-2]
    v_x[2:-1],        #v[k]
    v_x[1:-2],        #v[k-1]
    a_x[2:-1]         #a[k]
    )).T

y_x = s_x[3:]
print("A matrix: " + str(X_x.shape))
print("target matrix: " + str(np.array(y_x).shape))

X_y = np.vstack((
    s_y[2:-1],        #s[k]   
    s_y[1:-2],        #s[k-1]
    s_y[ :-3],        #s[k-2]
    v_y[2:-1],        #v[k]
    v_y[1:-2],        #v[k-1]
    a_y[2:-1]         #a[k]
    )).T

y_y = s_y[3:]
print("A matrix: " + str(X_y.shape))
print("target matrix: " + str(np.array(y_y).shape))



print("Linear regression with 6 parameters")
first_model = perform_linear_regression(X_x, y_x)
second_model = perform_linear_regression(X_y, y_y)


# Save both models in a pickle file
def save_model(model, model_name):
    model_file_path = os.path.join(saved_models_path, f'dist_model_5/{model_name}.pkl')
    
    with open(model_file_path, 'wb') as file:
        pickle.dump(model, file)
    
    print(f'Model "{model_name}" saved to: {model_file_path}')

save_model(first_model, 'first_model')
save_model(second_model, 'second_model')
