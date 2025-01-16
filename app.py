import os
import sys
from flask import Flask
from flask_jwt_extended import JWTManager
from extensions import db
from routes.user import user_bp
from routes.product import product_bp
from routes.auth import auth_bp
from routes.order import order_bp
import pymysql

pymysql.install_as_MySQLdb()

# 确保当前目录在 Python 的模块搜索路径中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 从 config.py 导入配置类
from config import Config

def create_app():
    # 创建 Flask 应用
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    jwt = JWTManager(app)  # 初始化 JWT

    # 注册蓝图
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(order_bp, url_prefix='/orders')
    return app


if __name__ == '__main__':
    # 创建应用并运行
    app = create_app()
    @app.route('/')
    def home():
        return "Welcome to Jade Commerce Backend API!"
    with app.app_context():
        db.create_all()  # 确保数据库表创建
    app.run(debug=True)
