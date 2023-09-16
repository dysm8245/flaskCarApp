from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=False, unique=True)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

    def __init__(self, first_name, last_name, email, username, password):
        self.id = self.set_id()
        self.token = self.set_token(24)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = self.set_password(password)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_token(self, length):
        return secrets.token_hex(24)
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
class CarCollection(db.Model):
    id = db.Column(db.String, primary_key = True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, make, model, year, user_token):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.year = year
        self.user_token = user_token

    def set_id(self):
        return secrets.token_urlsafe()
    
    
class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'make', 'model', 'year']

car_schema = CarSchema()
cars_schema = CarSchema(many=True)