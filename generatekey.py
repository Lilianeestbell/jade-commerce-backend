import secrets

# generate a random secret key
secret_key = secrets.token_hex(32)
print("SECRET_KEY:", secret_key)

# generate a random JWT_SECRET_KEY
jwt_secret_key = secrets.token_hex(32)
print("JWT_SECRET_KEY:", jwt_secret_key)
