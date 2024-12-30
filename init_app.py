from app import create_app
from models import db, user_datastore

app, _ = create_app()

#this file is for delete the database and create the new one with the default admin and user


def create_empty_tables():
    db.drop_all()
    db.create_all()

with app.app_context():
    create_empty_tables()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='user')
    db.session.commit()

    if not user_datastore.find_user(email="utsav.ashutosh@gmail.com"):
        admin_user=user_datastore.create_user(email="utsav.ashutosh@gmail.com", password="admin", username="admin")
        user_datastore.add_role_to_user(admin_user, "admin")

    if not user_datastore.find_user(email="user@a.com"):
        admin_user=user_datastore.create_user(email="user@a.com", password="user", username="user")
        user_datastore.add_role_to_user(admin_user, "user")

    db.session.commit()
        