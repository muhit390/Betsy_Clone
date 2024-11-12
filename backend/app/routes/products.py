from flask import Blueprint, jsonify, request
from ..models import Product
from ..extensions import db

bp = Blueprint('products', __name__, url_prefix='/products')

@bp.route('', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(
        user_id=data['user_id'],
        name=data['name'],
        category=data['category'],
        description=data['description'],
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created successfully"}), 201

@bp.route('', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "category": p.category, "price": p.price, "quantity": p.quantity} for p in products])

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