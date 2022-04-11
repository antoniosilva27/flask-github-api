from flask_sqlalchemy import SQLAlchemy
from config.app import app

db = SQLAlchemy()

db = SQLAlchemy(app)
