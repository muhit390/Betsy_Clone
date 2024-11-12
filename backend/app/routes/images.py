from flask import Blueprint, jsonify, request
from ..models import ProductImage
from ..extensions import db

images_bp = Blueprint('images', __name__)

@images_bp.route('/products/<int:product_id>/images', methods=['POST'])
def add_product_image(product_id):
    data = request.get_json()

    if not data.get('name'):
        return jsonify({"message": "Image name is required"}), 400

    new_image = ProductImage(
        product_id=product_id,
        name=data['name'],
        preview_image=data.get('preview_image', False)
    )
    
    try:
        db.session.add(new_image)
        db.session.commit()
        return jsonify({"message": "Image added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error adding image", "error": str(e)}), 500

@images_bp.route('/products/<int:product_id>/images', methods=['GET'])
def get_product_images(product_id):
    images = ProductImage.query.filter_by(product_id=product_id).all()
    
    if not images:
        return jsonify({"message": "No images found for this product"}), 404
    
    return jsonify([{
        "id": img.id,
        "name": img.name,
        "preview_image": img.preview_image
    } for img in images])

@images_bp.route('/products/<int:product_id>/images/<int:image_id>', methods=['PUT'])
def update_product_image(product_id, image_id):
    data = request.get_json()

    image = ProductImage.query.filter_by(id=image_id, product_id=product_id).first()
    
    if not image:
        return jsonify({"message": "Image not found"}), 404

    image.name = data.get('name', image.name)
    image.preview_image = data.get('preview_image', image.preview_image)
    
    try:
        db.session.commit()
        return jsonify({"message": "Image updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating image", "error": str(e)}), 500

@images_bp.route('/products/<int:product_id>/images/<int:image_id>', methods=['DELETE'])
def delete_product_image(product_id, image_id):
    image = ProductImage.query.filter_by(id=image_id, product_id=product_id).first()
    
    if not image:
        return jsonify({"message": "Image not found"}), 404

    try:
        db.session.delete(image)
        db.session.commit()
        return jsonify({"message": "Image deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting image", "error": str(e)}), 500