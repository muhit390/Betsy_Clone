from app import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text)
    description = db.Column(db.Text)
    price = db.Column(db.BigInteger, nullable=False)
    quantity = db.Column(db.BigInteger, nullable=False)

    reviews = db.relationship('Review', backref='product', lazy=True)
    product_images = db.relationship('ProductImage', backref='product', lazy=True)
    shopping_cart = db.relationship('ShoppingCart', backref='product', lazy=True)
    favorites = db.relationship('Favorite', backref='product', lazy=True)
