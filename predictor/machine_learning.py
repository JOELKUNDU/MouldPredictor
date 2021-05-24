from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
import sklearn.metrics as metrics
import matplotlib
import matplotlib.pyplot as plt
import joblib as jl
import os
import numpy as np
import predictor.database as database
from predictor.models import DBModelMetrics
from sklearn.model_selection import RandomizedSearchCV
from flask import flash

matplotlib.use('Agg')


class ModelMetrics:
    absolute_mean_error = 0.0
    modelScore = 0.0
    max_error = 0.0

    def printMetric(self):
        print(self.modelScore)
        print(self.max_error)
        print(self.absolute_mean_error)

    def savePerformance(self):
        DBModelMetrics(absolute_mean_error=self.absolute_mean_error,
                       model_score=self.modelScore,
                       max_error=self.max_error).save()

    def loadPerformance(self):
        perf = DBModelMetrics.query.filter_by(id=1).first()
        self.absolute_mean_error = perf.absolute_mean_error
        self.modelScore = perf.model_score
        self.max_error = perf.max_error


ml_metrics = ModelMetrics()

'''
BEST PARAMS {
'warm_start': True, 
'verbose': True, 
'solver': 'adam', 
'random_state': 1399, 
'max_iter': 125000, 
'learning_rate_init': 0.0001, 
'learning_rate': 'constant', 
'hidden_layer_sizes': (50, 50, 50), 
'alpha': 0.0001, 
'activation':'relu'
}
'''


def hyperTune():
    parameter_space = {
        'hidden_layer_sizes': [(50, 50, 50)],
        'activation': ['tanh', 'relu', 'logistic', 'identity'],
        'solver': ['sgd', 'adam', 'lbfgs'],
        'alpha':  np.arange(0.0001, 0.09, 100),
        'learning_rate': ['constant', 'adaptive', 'invscaling'],
        'learning_rate_init': np.arange(0.0001, 0.09, 100),
        'random_state': [1399],
        'warm_start': [True],
        'max_iter': [100000, 75000, 125000, 250000, 350000],
        'verbose': [True]
    }
    trained_model = MLPRegressor()
    X, y = database.get_datasets()
    X, X_test, y, y_test = train_test_split(X, y, test_size=0.33, random_state=1)
    clf = RandomizedSearchCV(trained_model, parameter_space, n_jobs=-1, cv=2, verbose=10)
    clf.fit(X, y)
    print('\n\n\nBEST PARAMS', clf.best_params_)
    print('\n\n\nResults', clf.cv_results_)

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
    jl.dump(clf, 'predictor/static/ML/config.joblib')
    flash('HyperTuning Complete', 'success')


def MLPRmodel(X_test):
    if os.path.exists('predictor/static/ML/config.joblib'):
        model = jl.load('predictor/static/ML/config.joblib')
    else:
        hyperTune()
        model = jl.load('predictor/static/ML/config.joblib')
    pred = model.predict(X_test)
    return pred


def getScore():
    trained_model = jl.load('predictor/static/ML/config.joblib')
    X, y = database.get_datasets()
    return trained_model.score(X, y)


def init_load_up():
    if not os.path.exists('predictor/static/ML/config.joblib'):
        hyperTune()
        X, y = database.get_datasets()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)
        pred = MLPRmodel(X_test)

        ml_metrics.absolute_mean_error = metrics.mean_absolute_error(y_test, pred)
        ml_metrics.modelScore = getScore()
        ml_metrics.max_error = metrics.max_error(y_test, pred)
        ml_metrics.savePerformance()

        plt.scatter(y_test, pred, color='b')
        plt.xlabel('Actual Weight')
        plt.ylabel('Predicted Weight')
        plt.title('Scatter Plot (Actual vs Predicted Part Weight)')
        # save the plot
        plt.savefig('predictor/static/ML/performance.png', bbox_inches='tight')
    ml_metrics.loadPerformance()


def retrain():
    X, y = database.get_datasets()
    # Splitting the data into test and trained data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)
    # Training the model and verifying the mean absolute error

    trained_model = jl.load('predictor/static/ML/config.joblib')

    trained_model.fit(X_train, y_train)
    pred = trained_model.predict(X_test)

    ml_metrics.absolute_mean_error = metrics.mean_absolute_error(y_test, pred)
    ml_metrics.modelScore = getScore()
    ml_metrics.max_error = metrics.max_error(y_test, pred)
    ml_metrics.savePerformance()

    pred = trained_model.predict(X)

    # Preparing the scatter plot of the model's prediction
    plt.scatter(y, pred, color='b')
    plt.xlabel('Actual Weight')
    plt.ylabel('Predicted Weight')
    plt.title('Scatter Plot (Actual vs Predicted Part Weight)')
    # save the plot
    plt.savefig('predictor/static/ML/performance.png', bbox_inches='tight')
    ml_metrics.loadPerformance()


def getPredict(Fill_time, Injection_pres, Holding_pres, Holding_time, Cooling_time,
               Mould_temp, Clamp_force, Shot_Weight,
               Mould_SA, Mould_vol, Cavity_SA, Cavity_vol,
               Melt_temp, Mat_density, Mat_GF, Mat_MMFR, part_weight):
    init_load_up()
    trained_model = jl.load('predictor/static/ML/config.joblib')
    X = [[Fill_time, Injection_pres, Holding_pres, Holding_time, Cooling_time,
          Mould_temp, Clamp_force, Shot_Weight,
          Mould_SA, Mould_vol, Cavity_SA, Cavity_vol,
          Melt_temp, Mat_density, Mat_GF, Mat_MMFR]]
    pred = trained_model.predict(X)
    pred[0] = abs(((pred[0]-part_weight)/part_weight)*100)
    return str(round(pred[0], 3))


def predict(
        Fill_time_min, Fill_time_max, Fill_time_res,
        Injection_pres_min, Injection_pres_max, Injection_pres_res,
        Holding_pres_min, Holding_pres_max, Holding_pres_res,
        Holding_time_min, Holding_time_max, Holding_time_res,
        Cooling_time_min, Cooling_time_max, Cooling_time_res,
        Mould_temp, Clamp_force, Shot_Weight,
        Mould_SA, Mould_vol, Cavity_SA, Cavity_vol,
        Mat_density, Melt_temp, Mat_GF, Mat_MMFR
):
    init_load_up()
    trained_model = jl.load('predictor/static/ML/config.joblib')
    weight_actual = Mould_vol * Mat_density
    print("\nweight:", weight_actual)
    first_pred = True
    param = []
    print('\r * Finding Parameters')
    for ft in range(Fill_time_min, Fill_time_max + 1, Fill_time_res):
        for ip in range(Injection_pres_min, Injection_pres_max + 1, Injection_pres_res):
            for hp in range(Holding_pres_min, Holding_pres_max + 1, Holding_pres_res):
                for ht in range(Holding_time_min, Holding_time_max + 1, Holding_time_res):
                    for ct in range(Cooling_time_min, Cooling_time_max + 1, Cooling_time_res):
                        X = [[ft, ip, hp, ht, ct,
                              Mould_temp, Clamp_force, Shot_Weight,
                              Mould_SA, Mould_vol, Cavity_SA, Cavity_vol,
                              Melt_temp, Mat_density, Mat_GF, Mat_MMFR]]
                        pred = trained_model.predict(X)
                        if weight_actual * 0.99 <= pred[0] <= weight_actual * 1.01:
                            if first_pred:
                                print("param:", X, "\nPred:", pred, "\nweight:", weight_actual)
                                parameter = X[0]
                                parameter.append(pred[0])
                                parameter.append(weight_actual)
                                param.append(parameter)

    try:
        minErrorParameter = []
        minErrorValue = abs(param[0][17] - param[0][16])
        for parameter in param:
            error = abs(parameter[17] - parameter[16])
            if abs(error < minErrorValue):
                minErrorParameter = parameter
                minErrorValue = error
                print(' * Current Minimum: ', parameter)
                print(' * min error value: ', minErrorValue)
        return minErrorParameter
    except:
        return []
