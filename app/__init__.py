from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_socketio import SocketIO
from datetime import datetime

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
    from app.models import User
    # Define the user_loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    #check connection
    @socketio.on('connect')
    def handle_connect():
        user = User.query.get(session.get('user_id'))
        if user:
            user.is_online = True
            user.last_active = datetime.utcnow()
            db.session.commit()
            socketio.emit('update_user_list', broadcast=True)
    
    @socketio.on('disconnect')
    def handle_disconnect():
        user = User.query.get(session.get('user_id'))
        if user:
            user.is_online = False
            db.session.commit()
            socketio.emit('update_user_list', broadcast=True)

    # Import and register routes
    with app.app_context():
        from . import routes

    return app
