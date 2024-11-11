from flask import Blueprint, request, jsonify
from models.user import User, db
from forms.login_form import LoginForm
from forms.signup_form import SignUpForm
from flask_login import current_user, login_user, logout_user
from flask_bcrypt import Bcrypt


auth_routes = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_routes.route('/')
def authenticate():
    if current_user.is_authenticated:
        return current_user.to_dict() 
    return {'errors': {'message': 'Unauthorized'}}, 401

@auth_routes.route('/unauthorized')
def unauthorized():
    return {'errors': {'message': 'Unauthorized'}}, 401

@auth_routes.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()

        login_user(user)
        return user.to_dict()
    
    return jsonify(form.errors), 401

@auth_routes.route('/logout')
def logout():
    logout_user()
    return {'message': 'User has been logged out.'}

@auth_routes('/users', methods=['POST'])
def create_user():
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        try:
            new_user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data
            )
            new_user.hashed_password = bcrypt.generate_password_hash(form.password.data)

            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User created successfully"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify(form.errors), 400



    