# app/models.py

from datetime import datetime, timezone
from . import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_online = db.Column(db.Boolean, default=False)
    last_active = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)
    # messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    # messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)
        # Explicitly specify the primaryjoin condition
    messages_sent = db.relationship(
        'Message',
        primaryjoin="User.id == Message.sender_id",  # Specify how the join is made
        backref='sender',
        lazy=True
    )
    messages_received = db.relationship(
        'Message',
        primaryjoin="User.id == Message.receiver_id",  # Specify how the join is made
        backref='receiver',
        lazy=True
    )
   
   
   
   
    # # Relationships, methods, etc.
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_online': self.is_online,
            'last_active': self.last_active.isoformat(),
            # 'is_active': self.is_active
        }
    

    # def deactivate(self):
    #     self.is_online = False
    #     db.session.commit()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



class ChatSession(db.Model):
    __tablename__ = 'chat_session'

    id = db.Column(db.Integer, primary_key=True)
    user_1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    user_1 = db.relationship('User', foreign_keys=[user_1_id], 
                              primaryjoin='User.id == ChatSession.user_1_id', 
                              backref='sessions_as_user_1')
    user_2 = db.relationship('User', foreign_keys=[user_2_id], 
                              primaryjoin='User.id == ChatSession.user_2_id', 
                              backref='sessions_as_user_2')



    def __repr__(self):
        return f"<ChatSession {self.id} between User {self.user_1_id} and User {self.user_2_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_1_id": self.user_1_id,
            "user_2_id": self.user_2_id,
            "started_at": self.started_at.isoformat(),
        }

    def __repr__(self):
        return f"<ChatSession {self.id} between {self.user_1_id} and {self.user_2_id}>"




def init_db():
    from app import db 