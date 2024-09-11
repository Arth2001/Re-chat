from flask import Flask, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_socketio import SocketIO
from flask_socketio import emit
from datetime import datetime,timezone


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
     # Import the User model and define the user_loader function
    
    with app.app_context():
        # from . import routes  # Import routes after app is initialized
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
                # user.deactivate()
                user.is_online = False
                # user.is_active = False
                db.session.commit()
                socketio.emit('update_user_list')



    # Import and register routes
    with app.app_context():
        from . import routes

    return app