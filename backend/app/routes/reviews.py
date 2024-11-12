from flask import Blueprint, jsonify, request
from ..models import Review
from ..extensions import db

bp = Blueprint('reviews', __name__, url_prefix='/products/<int:product_id>/reviews')

@bp.route('', methods=['POST'])
def add_review(product_id):
    data = request.get_json()
    new_review = Review(
        product_id=product_id,
        user_id=data['user_id'],
        review=data['review'],
        rating=data['rating']
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "Review added successfully"}), 201

@bp.route('', methods=['GET'])
def get_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify([{"id": r.id, "user_id": r.user_id, "review": r.review, "rating": r.rating} for r in reviews])