from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config.db import db
from config.app import app
from models.user import User

import requests


@app.route('/')
@app.route('/users/')
def users():
    users = User.query.all()
    return render_template('home.html', users=users)

#  Get user by id
@app.route('/user/<id>', methods=['GET'])
def get_user_id(id):
    user = User.query.filter_by(id=id).first()
    return jsonify(user)

# Create a new user
@app.route('/create', methods=['POST', 'GET'])
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
        return redirect("/", code=302)
        
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
        return redirect("/", code=302)
    except Exception as e:
        return 'error'

if __name__ == "__main__":
    create_user('dragoleta')
    create_user('antoniosilva27')
    create_user('MoisesAbraao')
    # db.create_all()
    # db.session.add_all(users)
    # db.session.commit()
    app.run()