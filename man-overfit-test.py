"""
This script verifies if the model is over-trained
(training score higher than testing by a huge margin)
"""

import joblib as jl
import predictor.database as database
from sklearn.model_selection import train_test_split

X, y = database.get_datasets()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)

trained_model = jl.load('predictor/static/ML/config.joblib')

print('Training Score:', trained_model.score(X_train, y_train))
print('Testing Score:', trained_model.score(X_test, y_test))
print('Full Score:', trained_model.score(X, y))
