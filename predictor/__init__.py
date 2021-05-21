from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


class AppState(object):
    _serverState = False

    def __init__(self):
        self._serverState = False

    def serverModeOn(self):
        self._serverState = True

    def serverModeOff(self):
        self._serverState = False

    def queryServerState(self):
        if self._serverState:
            return True
        else:
            return False


state = AppState()
modulePath = os.path.abspath(__name__)
csvPath = 'static/client/csv/'
uploadPath = 'uploads/'
clientUploadPath = os.path.normpath(os.path.join(modulePath,uploadPath))
clientCSVPath = os.path.normpath(os.path.join(modulePath, csvPath))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = '9a257ea9a3b0b646c25ec6f8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CLIENT_CSV'] = clientCSVPath
app.config['UPLOADS'] = clientUploadPath
db = SQLAlchemy(app)


from predictor import routes





