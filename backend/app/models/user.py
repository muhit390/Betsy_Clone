from extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False) #added but removed if not wanted elliot
    username = db.Column(db.String(255), unique=True, nullable=False)  # This should be 'username'
    hashed_password = db.Column(db.String(255), nullable=False)

    products = db.relationship('Product', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    shopping_cart = db.relationship('ShoppingCart', backref='user', lazy=True)

    def set_password(self, password):
        self.hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)

def to_dict(self):
    return {
        'id': self.id,
        'username': self.username,
        'email': self.email
    }