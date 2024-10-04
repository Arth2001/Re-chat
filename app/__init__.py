from flask import Flask, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_socketio import emit
from datetime import datetime, timezone

# Initialize the Bcrypt, SQLAlchemy, and LoginManager instances
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)  # Initialize SocketIO with the app
    
    login_manager.login_view = 'login'  # Redirect to login page if user needs to log in
    
    with app.app_context():
        from .models import init_db  # Use the delayed model import
        init_db() 

    from app.models import User
    from app.utils import get_online_users

    # Define the user_loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @socketio.on('connect')
    def handle_connect():
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user and user.is_active:  # Check if user is active
                user.is_online = True
                user.is_active = True
                user.last_active = datetime.now(timezone.utc)
                db.session.commit()
                socketio.emit('update_user_list')

    @socketio.on('disconnect')
    def handle_disconnect():
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                user.is_online = False
                db.session.commit()
                socketio.emit('update_user_list')

    # Handle joining a private room
    @socketio.on('join_room')
    def handle_join_room(data):
        room = data['room']
        join_room(room)
        send(f'User has joined the room {room}', to=room)

    # Handle private message sending
    @socketio.on('private_message')
    def handle_private_message(data):
        room = data['room']
        message = data['message']
        user_id = session.get('user_id')  # Get the sender's user ID
        if user_id:
            send({'message': message, 'senderId': user_id}, to=room)

    # Import and register routes
    with app.app_context():
        from . import routes

    return app

# In your main.py (or equivalent)
if __name__ == "__main__":
    app = create_app()
    socketio.run(app, debug=True)
