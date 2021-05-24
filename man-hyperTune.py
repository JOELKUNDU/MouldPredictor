"""
This script will auto-hyper tune the model and then retrain it without opening the app
"""
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import predictor.machine_learning as ml
import predictor.database as database
import joblib as jl
import numpy as np

if __name__ == '__main__':
    parameter_space = {
        'hidden_layer_sizes': [(50, 50, 50)],
        'activation': ['tanh', 'relu', 'logistic', 'identity'],
        'solver': ['sgd', 'adam', 'lbfgs'],
        'alpha':  np.arange(0.0001, 0.09, 100),
        'learning_rate': ['constant', 'adaptive', 'invscaling'],
        'learning_rate_init': np.arange(0.0001, 0.09, 100),
        'random_state': [1399],
        'warm_start': [True],
        'max_iter': [100000, 75000, 125000],
        'verbose': [True]
    }
    trained_model = MLPRegressor()
    X, y = database.get_datasets()
    X, X_test, y, y_test = train_test_split(X, y, test_size=0.33, random_state=1)
    clf = GridSearchCV(trained_model, parameter_space, n_jobs=-1, cv=2, verbose=10)
    clf.fit(X, y)
    print('\n\n\nBEST PARAMS', clf.best_params_)
    print('\n\n\nResults', clf.cv_results_)
    jl.dump(clf, 'predictor/static/ML/config.joblib')
