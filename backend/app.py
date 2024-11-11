from flask import Flask, jsonify, request
from config import Config
from extensions import db , migrate
from flask_bcrypt import Bcrypt

from models import User, Product, Review, ProductImage, ShoppingCart, Favorite

app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)


db.init_app(app)
migrate.init_app(app, db)




# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Etsy Clone!"})


# Routes for User Model



# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    try:
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
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "first_name": u.first_name, "last_name": u.last_name} for u in users])

# Get a single user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify({"id": user.id, "username": user.username, "first_name": user.first_name, "last_name": user.last_name})
    return jsonify({"message": "User not found"}), 404




# Routes for Product Model

# Create a new product
@app.route('/products', methods=['POST'])
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

# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "category": p.category, "price": p.price, "quantity": p.quantity} for p in products])

# Get a product by ID
@app.route('/products/<int:id>', methods=['GET'])
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




# Routes for Review Model



# Add a review to a product
@app.route('/products/<int:product_id>/reviews', methods=['POST'])
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

# Get all reviews for a product
@app.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify([{"id": r.id, "user_id": r.user_id, "review": r.review, "rating": r.rating} for r in reviews])




# Routes for ProductImage Model



# Add an image to a product
@app.route('/products/<int:product_id>/images', methods=['POST'])
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

# Get all images for a product
@app.route('/products/<int:product_id>/images', methods=['GET'])
def get_product_images(product_id):
    images = ProductImage.query.filter_by(product_id=product_id).all()
    return jsonify([{"id": img.id, "name": img.name, "preview_image": img.preview_image} for img in images])




# Routes for ShoppingCart Model




# Add a product to a user's shopping cart
@app.route('/users/<int:user_id>/cart', methods=['POST'])
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
@app.route('/users/<int:user_id>/cart', methods=['GET'])
def get_cart(user_id):
    cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()
    return jsonify([{"product_id": item.product_id} for item in cart_items])





# Routes for Favorite Model



# Add a product to user's favorites
@app.route('/users/<int:user_id>/favorites', methods=['POST'])
def add_to_favorites(user_id):
    data = request.get_json()
    new_favorite = Favorite(
        user_id=user_id,
        product_id=data['product_id']
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "Product added to favorites"}), 201

# Get all favorite products of a user
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([{"product_id": fav.product_id} for fav in favorites])




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 ,debug=True)
