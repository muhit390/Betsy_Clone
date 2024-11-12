# models/product_image.py
from app import db

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    id = db.Column(db.BigInteger, primary_key=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'), nullable=False)
    name = db.Column(db.String(255))
    preview_image = db.Column(db.Boolean, default=False)
