from extensions import db

class User(db.Model):
    __tablename__ = "users"
    id=db.Column(db.BigInteger , primary_key=True)
    first_name=db.Column(db.String(255) , nullable=False)
    last_name=db.Column(db.String(255) , nullable=False)
    user_name=db.Column(db.String(255) , unique = True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)


    products = db.relationship('Product', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    shopping_cart = db.relationship('ShoppingCart', backref='user', lazy=True)
