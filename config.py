# config.py

import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://messaging_user:secure_password@localhost/messaging_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    HASH_METHOD = 'sha256'