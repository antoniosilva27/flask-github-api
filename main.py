from app import app, db, users, User, create_user

if __name__ == "__main__":
    create_user('dragoleta')
    db.create_all()
    # db.session.add_all(users)
    # db.session.commit()
    app.run()
