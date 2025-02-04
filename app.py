import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from utils.decorators import role_required

# make sure the current directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# import the necessary modules
from config import Config
from routes.user import user_bp
from routes.product import product_bp
from routes.auth import auth_bp
from routes.order import order_bp
from routes.shoppingCart import cart_bp
from extensions import db

migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # load the configuration from the Config class in config.py
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)  # initialize the migration engine
    jwt.init_app(app)  # initialize JWT

    # register the blueprints
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(cart_bp, url_prefix='/cart')

    @app.route('/')
    def home():
        return "Welcome to Jade Commerce Backend API!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
