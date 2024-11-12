from app import db

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.BigInteger, primary_key=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    review = db.Column(db.Text)
    rating = db.Column(db.BigInteger, nullable=False)
