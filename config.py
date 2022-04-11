from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__, template_folder='template')
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///github.sqlite3'

db = SQLAlchemy(app)
