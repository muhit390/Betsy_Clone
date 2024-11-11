# models/shopping_cart.py
from app import db

class ShoppingCart(db.Model):
    __tablename__ = 'shopping_cart'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'), primary_key=True)
