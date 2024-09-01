from datetime import datetime
from .models import User
from . import db

def set_user_online(user_id: int):
    user = User.query.get(user_id)
    if user:
        user.is_online = True
        db.session.commit()

def set_user_offline(user_id: int):
    user = User.query.get(user_id)
    if user:
        user.is_online = False
        db.session.commit()

def update_last_active(user_id: int):
    user = User.query.get(user_id)
    if user:
        user.last_active = datetime.utcnow()
        db.session.commit()

def get_user_by_username(username: str):
    return User.query.filter_by(username=username).first()

def get_online_users():
    return User.query.filter_by(is_online=True).all()
