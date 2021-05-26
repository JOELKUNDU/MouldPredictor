"""
This script will auto-hyper tune the model and then retrain it without opening the app
"""
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import predictor.database as database
from predictor.machine_learning import ml_metrics, metrics, getScore
import joblib as jl
import numpy as np
import matplotlib as plt

if __name__ == '__main__':
    parameter_space = {
        'hidden_layer_sizes': [(64, 64, 64,), (256, 256, 256,), (125, 125, 125,)],
        'activation': ['tanh', 'relu', 'logistic', 'identity'],
        'solver': ['sgd', 'adam', 'lbfgs'],
        'learning_rate_init': np.arange(0.0001, 0.001, 0.00002),
        'learning_rate': ['constant', 'adaptive', 'invscaling'],
        'learning_rate_init': np.arange(0.0001, 0.001, 0.00002),
        'random_state': [1399],
        'warm_start': [True],
        'max_iter': np.arange(100, 250000, 1),
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
    pred = clf.predict(X_test)

    ml_metrics.absolute_mean_error = metrics.mean_absolute_error(y_test, pred)
    ml_metrics.modelScore = getScore()
    ml_metrics.max_error = metrics.max_error(y_test, pred)
    ml_metrics.savePerformance()

    pred = clf.predict(X)

    plt.scatter(y, pred, color='b')
    plt.xlabel('Actual Weight')
    plt.ylabel('Predicted Weight')
    plt.title('Scatter Plot (Actual vs Predicted Part Weight)')
    plt.savefig('predictor/static/ML/performance.png', bbox_inches='tight')
    ml_metrics.loadPerformance()
    ml_metrics.printMetric()
    jl.dump(clf, 'predictor/static/ML/config.joblib')
