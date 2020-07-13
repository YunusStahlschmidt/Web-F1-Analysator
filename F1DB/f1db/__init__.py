from flask import Flask
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b61fc7bf8219a999f17de110287f65ce'
db = mysql.connector.connect(host="localhost",
                             user="root",
                             password="MDBpPs2020fSQL",
                             database="f1db")
cursor = db.cursor(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from F1DB.f1db import routes
