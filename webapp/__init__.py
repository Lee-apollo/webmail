from flask import Flask
import sys

app = Flask(__name__)
app.config.from_object('config')

sys.path.append("./webapp")

from webapp import views
from webapp import db_interface
