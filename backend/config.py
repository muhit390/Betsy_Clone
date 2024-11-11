# config.py
class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///etsy_clone.db'  # SQLite database file
    SECRET_KEY = 'e39b073bc5f7d4f8a2bc1d879a8d06e1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
