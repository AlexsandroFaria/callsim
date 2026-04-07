from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///controlechamado.db'
app.config['SECRET_KEY'] = '4856267994003ddf2c9d3c39'
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)
login_manager.login_view = "/"
login_manager.login_message = "Por favor, realize o Login!"
login_manager.login_message_category = "info"

from CallSim import routes