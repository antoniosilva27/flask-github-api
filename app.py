from flask import jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from models import User
from config import db, app
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
def create_user():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        api_request = requests.get(f"https://api.github.com/users/{request.form['username']}").json()
        try:
            user = User(name=api_request['name'], 
                        login=api_request['login'],
                        public_repos=api_request['public_repos'],
                        followers=api_request['followers'],
                        following=api_request['following'],
                        profile_image=api_request['avatar_url'],
                        html_url=api_request['html_url']
                        )

            db.session.add(user)
            db.session.commit()
            return render_template('register.html')
            
        except Exception as e:
            message = 'User already inserted into database'
            return render_template('register.html', message=message)

# Update

@app.route('/update/<id>', methods=['PUT', 'GET'])
def update_user(id):
    user = User.query.filter_by(id=id).first()
    api_request = requests.get(f"https://api.github.com/users/{user.login}").json()

    try:
        if ('name' in api_request):
            user.name = api_request['name']
        if ('login' in api_request):    
            user.login = api_request['login']
        if ('public_repos' in api_request):
            user.public_repos = api_request['public_repos']
        if ('followers' in api_request):
            user.followers = api_request['followers']
        if ('following' in api_request):
            user.following = api_request['following'] 
        if ('profile_image' in api_request):
            user.profile_image = api_request['avatar_url']
        if ('html_url' in api_request):
            user.html_url = api_request['html_url']
            
        db.session.commit()
        return redirect("/", code=302)
    except Exception as e:
        print(e)
        message = 'User already updated'
        return redirect("/", code=302, message=message)

@app.route('/delete/<int:id>', methods=['DELETE', 'GET'])
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect("/", code=302)
    except Exception as e:
        message = 'User already deleted'
        return redirect("/", code=302, message=message)

if __name__ == "__main__":
    db.create_all()
    app.run()