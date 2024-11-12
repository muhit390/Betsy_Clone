from flask import Blueprint, jsonify, request
from app.models import Favorite, Product, db

favorites_bp = Blueprint('favorites', __name__)

# Add a product to user's favorites
@favorites_bp.route('/users/<int:user_id>/favorites', methods=['POST'])
def add_to_favorites(user_id):
    data = request.get_json()
    new_favorite = Favorite(
        user_id=user_id,
        product_id=data['product_id']
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "Product added to favorites"}), 201

# Get all favorite products of a user
@favorites_bp.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    favorite_products = []
    for fav in favorites:
        product = Product.query.get(fav.product_id)
        if product:
            favorite_products.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price
            })
    return jsonify(favorite_products)

# Remove a product from the user's favorites
@favorites_bp.route('/users/<int:user_id>/favorites/<int:product_id>', methods=['DELETE'])
def remove_from_favorites(user_id, product_id):
    favorite = Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Product removed from favorites"}), 200
    return jsonify({"message": "Product not found in favorites"}), 404