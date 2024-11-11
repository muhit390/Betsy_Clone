from flask import Blueprint, request
from models.user import User
from flask_login import current_user, login_user, logout_user, login_required


auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/')
def authenticate():
    if current_user.is_authenticated:
        return current_user.to_dict() 
    return {'errors': {'message': 'Unauthorized'}}, 401
    