from dataclasses import dataclass
from config import db

@dataclass
class User(db.Model):
    id: int
    login: str
    name: str
    public_repos: int
    followers: int
    following: int
    profile_image: str
    

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    login = db.Column(db.String(200), unique=True)
    name = db.Column(db.String(200))
    public_repos = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    following = db.Column(db.Integer)
    profile_image = db.Column(db.String)


