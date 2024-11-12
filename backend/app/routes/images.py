from flask import Blueprint, jsonify, request
from ..models import ProductImage
from ..extensions import db

images_bp = Blueprint('images', __name__)

@images_bp.route('/products/<int:product_id>/images', methods=['POST'])
def add_product_image(product_id):
    data = request.get_json()
    new_image = ProductImage(
        product_id=product_id,
        name=data['name'],
        preview_image=data.get('preview_image', False)
    )
    db.session.add(new_image)
    db.session.commit()
    return jsonify({"message": "Image added successfully"}), 201

@images_bp.route('/products/<int:product_id>/images', methods=['GET'])
def get_product_images(product_id):
    images = ProductImage.query.filter_by(product_id=product_id).all()
    return jsonify([{"id": img.id, "name": img.name, "preview_image": img.preview_image} for img in images])