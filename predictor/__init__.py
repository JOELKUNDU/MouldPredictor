from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import json
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


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
clientUploadPath = os.path.normpath(os.path.join(modulePath, uploadPath))
clientCSVPath = os.path.normpath(os.path.join(modulePath, csvPath))


app = Flask(__name__)
configPath = os.path.join(app.root_path, 'config.json')
config = open(configPath)
data = json.load(config)
if data["ServerMode"] == "True":
    print(" * Running in SERVER MODE")
    state.serverModeOn()

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = '9a257ea9a3b0b646c25ec6f8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CLIENT_CSV'] = clientCSVPath
app.config['UPLOADS'] = clientUploadPath
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


from predictor import routes





