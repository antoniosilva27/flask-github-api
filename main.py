from app import app, db, users, User

if __name__ == "__main__":
    users = User(email="drake@drake.com"), User(email="josh@josh.com")
    db.create_all()
    db.session.add_all(users)
    db.session.commit()
    app.run()
