from flask import Blueprint, jsonify, request
from ..models import Product
from ..extensions import db

bp = Blueprint('products', __name__, url_prefix='/products')

@bp.route('', methods=['POST'])
def create_product():
    data = request.get_json()

    if not all(field in data for field in ['user_id', 'name', 'category', 'description', 'price', 'quantity']):
        return jsonify({"message": "Missing required fields"}), 400

    new_product = Product(
        user_id=data['user_id'],
        name=data['name'],
        category=data['category'],
        description=data['description'],
        price=data['price'],
        quantity=data['quantity']
    )
    
    try:
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating product", "error": str(e)}), 500

@bp.route('', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "id": p.id, 
        "name": p.name, 
        "category": p.category, 
        "price": p.price, 
        "quantity": p.quantity
    } for p in products])

@bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity
        })
    return jsonify({"message": "Product not found"}), 404

@bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()

    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    product.name = data.get('name', product.name)
    product.category = data.get('category', product.category)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.quantity = data.get('quantity', product.quantity)
    
    try:
        db.session.commit()
        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating product", "error": str(e)}), 500

@bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):

    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting product", "error": str(e)}), 500