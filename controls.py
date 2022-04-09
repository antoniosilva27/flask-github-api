from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests
from dataclasses import dataclass

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///github.sqlite3'
db = SQLAlchemy(app)

# @app.route('/')
# def home():
#     return render_template('home.html')
@dataclass
class User(db.Model):
    id: int
    login: str
    name: str
    public_repos: int
    followers: int
    following: int

    id = db.Column(db.Integer(), primary_key=True, auto_increment=True)
    login = db.Column(db.String(200), unique=True)
    name = db.Column(db.String(200))
    public_repos = db.Column(db.Integer())
    followers = db.Column(db.Integer())
    following = db.Column(db.Integer())

@app.route('/')
@app.route('/users/')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

#  Get user by id
@app.route('/user/<id>', methods=['GET'])
def get_user_id(id):
    user = User.query.filter_by(id=id).first()
    return jsonify(user)

# Create a new user
@app.route('/create', methods=['POST'])
def create_user(username):
    api_request = requests.get(f"https://api.github.com/users/{username}").json()

    try:
        user = User(name=api_request['name'], 
                    login=api_request['login'],
                    public_repos=api_request['public_repos'],
                    followers=api_request['followers'],
                    following=api_request['following'],
                    )

        db.session.add(user)
        db.session.commit()
        return jsonify(user)
        
    except Exception as e:
        print(e)
        return 'Error'

# Update

@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.filter_by(id=id).first()
    body = request.get_json()
    try:
        if ('name' in body):
            user.name = body['name']
        if ('login' in body):    
            user.login = body['login']

        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return 'Error'

@app.route('/delete/<int:id>', methods=['DELETE', 'GET'])
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return users()
    except Exception as e:
        flash('Error', e)

if __name__ == "__main__":
    create_user('dragoleta')
    # db.create_all()
    # db.session.add_all(users)
    # db.session.commit()
    app.run()