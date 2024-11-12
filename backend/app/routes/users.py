from flask import Blueprint, jsonify, request
from ..models import User
from ..extensions import db

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username'],
        hashed_password=data['hashed_password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "first_name": u.first_name, "last_name": u.last_name} for u in users])

@bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify({"id": user.id, "username": user.username, "first_name": user.first_name, "last_name": user.last_name})
    return jsonify({"message": "User not found"}), 404