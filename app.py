import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from utils.decorators import role_required

# 确保当前目录在 Python 的模块搜索路径中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 从 config.py 导入配置类
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

    # 加载配置
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)  # 初始化数据库迁移
    jwt.init_app(app)  # 初始化 JWT

    # 注册蓝图
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
