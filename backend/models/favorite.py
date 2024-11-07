# models/favorite.py
from app import db

class Favorite(db.Model):
    __tablename__ = 'favorites'
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), primary_key=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'), primary_key=True)
