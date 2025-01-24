from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import jsonify

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()  # 验证 JWT 是否有效
                claims = get_jwt()  # 提取 JWT claims
                print(f"Claims: {claims}")  # 打印 claims 以便调试
                user_identity = claims.get("sub")  # 从 claims 中提取 identity（sub 字段）
                user_role = user_identity.get("role")  # 从 identity 中提取 role
                print(f"user_role: {user_role}, required_role: {required_role}")

                if user_role != required_role:
                    return jsonify({"error": "You do not have permission to perform this action."}), 403

                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error in role_required: {str(e)}")  # 打印具体异常以调试
                return jsonify({"error": "Invalid or missing token"}), 401
        return wrapper
    return decorator

