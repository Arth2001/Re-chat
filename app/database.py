# app/database.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the given Flask app."""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Create database tables

def get_db():
    """Get the database instance."""
    return db
