from flask import Flask
from .config import Config
from .extensions import db, migrate
from .routes import users, products, reviews, images, shopping_cart, favorites

def create_app():
    app = Flask(__name__, static_folder='../react-app/build', static_url_path='/')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(users.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(reviews.bp)
    app.register_blueprint(images.bp)
    app.register_blueprint(shopping_cart.bp)
    app.register_blueprint(favorites.bp)

    return app

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    if path == 'favicon.ico':
        return app.send_from_directory('public', 'favicon.ico')
    return app.send_static_file('index.html')