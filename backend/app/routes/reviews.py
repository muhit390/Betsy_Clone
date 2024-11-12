from flask import Blueprint, jsonify, request
from ..models import Review
from ..extensions import db

bp = Blueprint('reviews', __name__, url_prefix='/products/<int:product_id>/reviews')

@bp.route('', methods=['POST'])
def add_review(product_id):
    data = request.get_json()
    
    if not data.get('user_id') or not data.get('review') or not data.get('rating'):
        return jsonify({"message": "Missing required fields"}), 400

    new_review = Review(
        product_id=product_id,
        user_id=data['user_id'],
        review=data['review'],
        rating=data['rating']
    )
    
    try:
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error adding review", "error": str(e)}), 500

@bp.route('', methods=['GET'])
def get_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    
    if not reviews:
        return jsonify({"message": "No reviews found for this product"}), 404
    
    return jsonify([{
        "id": r.id,
        "user_id": r.user_id,
        "review": r.review,
        "rating": r.rating
    } for r in reviews])

@bp.route('/<int:review_id>', methods=['PUT'])
def update_review(product_id, review_id):
    data = request.get_json()

    review = Review.query.filter_by(id=review_id, product_id=product_id).first()
    
    if not review:
        return jsonify({"message": "Review not found"}), 404

    review.review = data.get('review', review.review)
    review.rating = data.get('rating', review.rating)
    
    try:
        db.session.commit()
        return jsonify({"message": "Review updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating review", "error": str(e)}), 500

@bp.route('/<int:review_id>', methods=['DELETE'])
def delete_review(product_id, review_id):

    review = Review.query.filter_by(id=review_id, product_id=product_id).first()
    
    if not review:
        return jsonify({"message": "Review not found"}), 404

    try:
        db.session.delete(review)
        db.session.commit()
        return jsonify({"message": "Review deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting review", "error": str(e)}), 500