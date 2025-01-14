import secrets

# 生成一个随机的 SECRET_KEY
secret_key = secrets.token_hex(32)
print("SECRET_KEY:", secret_key)

# 生成一个随机的 JWT_SECRET_KEY
jwt_secret_key = secrets.token_hex(32)
print("JWT_SECRET_KEY:", jwt_secret_key)
