from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('users', __name__)

# get all users
@user_bp.route('/all', methods=['GET'])
def get_all_users():
    users = User.query.filter_by(is_deleted=False).all()
    return {"users": [user.to_dict() for user in users]}, 200

# get all users with pagination
@user_bp.route('/', methods=['GET'])
def list_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '', type=str)

    query = User.query.filter(User.is_deleted == False)
    if search:
        query = query.filter(User.username.contains(search))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "users": [user.to_dict() for user in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }), 200

# get user by id
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id, is_deleted=False).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()

    # verify required fields
    if not all(k in data for k in ("username", "email", "password")):
        return {"error": "Missing username, email, or password"}, 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201
    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Username or email already exists"}, 400
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


# delete user (soft delete)
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user or user.is_deleted:
        return {"message": "User not found or already deleted"}, 404

    user.is_deleted = True
    db.session.commit()
    return {"message": f"User with id {user_id} has been logically deleted."}, 200

# update user
@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    print("JWT Identity:", current_user)
    if current_user["id"] != user_id:
        return jsonify({"error": "Permission denied"}), 403
    data = request.get_json()
    user = User.query.filter_by(id=user_id, is_deleted=False).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    db.session.commit()
    return jsonify({"message": "User updated successfully", "user": user.to_dict()}), 200

# # user login
# @user_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()

#     if not all(k in data for k in ("email", "password")):
#         return jsonify({"error": "Missing email or password"}), 400

#     user = User.query.filter_by(email=data['email'], is_deleted=False).first()
#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     if not check_password_hash(user.password, data['password']):
#         return jsonify({"error": "Invalid password"}), 401

#     return jsonify({
#         "message": "Login successful",
#         "user": user.to_dict()
#     }), 200
