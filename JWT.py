import secrets

jwt_secret_key = secrets.token_hex(32)
print(jwt_secret_key)