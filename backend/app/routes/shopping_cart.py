from flask import Blueprint, jsonify, request
from app.models import ShoppingCart, Product, db

shopping_cart_bp = Blueprint('shopping_cart', __name__)

# Add a product to a user's shopping cart
@shopping_cart_bp.route('/users/<int:user_id>/cart', methods=['POST'])
def add_to_cart(user_id):
    data = request.get_json()
    new_cart_item = ShoppingCart(
        user_id=user_id,
        product_id=data['product_id']
    )
    db.session.add(new_cart_item)
    db.session.commit()
    return jsonify({"message": "Product added to cart"}), 201

# Get all products in a user's shopping cart
@shopping_cart_bp.route('/users/<int:user_id>/cart', methods=['GET'])
def get_cart(user_id):
    cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()
    cart_products = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            cart_products.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity_in_cart": 1  # Assuming only 1 quantity of each item per cart
            })
    return jsonify(cart_products)

# Remove a product from the user's shopping cart
@shopping_cart_bp.route('/users/<int:user_id>/cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart(user_id, product_id):
    cart_item = ShoppingCart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Product removed from cart"}), 200
    return jsonify({"message": "Item not found in cart"}), 404

# Checkout (complete the purchase)
@shopping_cart_bp.route('/users/<int:user_id>/checkout', methods=['POST'])
def checkout(user_id):
    cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400
    
    # Process the purchase (this is a simple example)
    # Here you could implement actual payment logic
    
    # Empty the cart after successful purchase
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()
    
    return jsonify({"message": "Checkout successful. Thank you for your purchase!"}), 200