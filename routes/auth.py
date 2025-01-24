from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies, get_jwt_identity
from models.user import User
from utils.decorators import role_required

auth_bp = Blueprint('auth', __name__)

# 用户登录
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # 查找用户
    user = User.query.filter_by(email=email, is_deleted=False).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401
    identity = {"id": user.id, "email": user.email, "role": user.role}
    print("Identity:", identity)
    # 创建 JWT Token
    access_token = create_access_token(identity=identity)
    return jsonify({"message": "Login successful", "access_token": access_token}), 200

# 用户登出
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"message": "Logged out successfully"})
    # 清除 JWT Token
    unset_jwt_cookies(response)
    return response, 200

# admin only route
@auth_bp.route('/admin-only', methods=['GET'])
@jwt_required()
@role_required('admin')  # 使用装饰器限制角色
def admin_only_route():
    identity = get_jwt_identity()
    print("JWT Identity:", identity)  # 打印当前身份信息
    return jsonify({"message": "Welcome, Admin!"}), 200