# config.py
class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///etsy_clone.db'  # SQLite database file
    SQLALCHEMY_TRACK_MODIFICATIONS = False
