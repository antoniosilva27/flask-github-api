from dataclasses import dataclass
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

app = Flask(__name__)
db = SQLAlchemy(app)

@dataclass
class User(db.Model):
    id: int
    email: str

    id = db.Column(db.Integer(), primary_key=True, auto_increment=True)
    email = db.Column(db.String(200), unique=True)

@app.route('/users/')
def users():
    users = User.query.all()
    return jsonify(users)

