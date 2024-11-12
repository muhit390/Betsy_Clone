from flask import Flask
from .config import Config
from .extensions import db, migrate
from .routes import users, products, reviews, images, shopping_cart, favorites

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(users.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(reviews.bp)
    app.register_blueprint(images.bp)
    app.register_blueprint(shopping_cart.bp)
    app.register_blueprint(favorites.bp)

    return app