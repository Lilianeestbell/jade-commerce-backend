from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies, get_jwt_identity
from models.user import User
from utils.decorators import role_required

auth_bp = Blueprint('auth', __name__)

# login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # search for the user in the database
    user = User.query.filter_by(email=email, is_deleted=False).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401
    identity = {"id": user.id, "email": user.email, "role": user.role}
    print("Identity:", identity)
    # create JWT Token
    access_token = create_access_token(identity=identity)
    return jsonify({"message": "Login successful", "access_token": access_token}), 200

# logout route
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"message": "Logged out successfully"})
    # clear JWT Token
    unset_jwt_cookies(response)
    return response, 200

# admin only route
@auth_bp.route('/admin-only', methods=['GET'])
@jwt_required()
@role_required('admin')  # use the role_required decorator to restrict access to admin users only
def admin_only_route():
    identity = get_jwt_identity()
    print("JWT Identity:", identity) # print the JWT Identity
    return jsonify({"message": "Welcome, Admin!"}), 200