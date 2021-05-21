"""
This script will auto-hyper tune the model and then retrain it without opening the app
"""
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import predictor.machine_learning as ml
import predictor.database as database
import joblib as jl

if __name__ == '__main__':
    parameter_space = {
        'hidden_layer_sizes': [(50, 50, 50)],
        'activation': ['tanh', 'relu', 'logistic', 'identity'],
        'solver': ['sgd', 'adam', 'lbfgs'],
        'alpha':  [0.001, 0.01, 0.1, 0.0001,
                   0.002, 0.02, 0.2, 0.0002,
                   0.003, 0.03, 0.3, 0.0003,
                   0.004, 0.04, 0.4, 0.0004,
                   0.005, 0.05, 0.5, 0.0005,
                   0.006, 0.06, 0.6, 0.0006,
                   0.007, 0.07, 0.7, 0.0007,
                   0.008, 0.08, 0.8, 0.0008,
                   0.009, 0.09, 0.9, 0.0009],
        'learning_rate': ['constant', 'adaptive', 'invscaling'],
        'learning_rate_init': [0.001, 0.01, 0.1, 0.0001,
                               0.002, 0.02, 0.2, 0.0002,
                               0.003, 0.03, 0.3, 0.0003,
                               0.004, 0.04, 0.4, 0.0004,
                               0.005, 0.05, 0.5, 0.0005,
                               0.006, 0.06, 0.6, 0.0006,
                               0.007, 0.07, 0.7, 0.0007,
                               0.008, 0.08, 0.8, 0.0008,
                               0.009, 0.09, 0.9, 0.0009],
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
    ml.retrain()
