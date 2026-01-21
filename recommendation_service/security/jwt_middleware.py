# security/jwt_middleware.py
from flask import request, g
from functools import wraps
import jwt
from config import Config

with open(Config.RSA_PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = f.read()

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth:
            return {"error": "Missing Authorization header"}, 401

        parts = auth.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return {"error": "Invalid Authorization header format"}, 401

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                PUBLIC_KEY,
                algorithms=["RS256"],
                options={"verify_aud": False},
                leeway=30
            )
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}, 401
        except jwt.InvalidTokenError as e:
            return {"error": "Invalid token", "message": str(e)}, 401

        g.userId = payload.get("userId")
        g.user_roles = payload.get("scope", "").split()
        g.jwt_token = token  # <-- conservé pour les appels internes

        if not g.userId:
            return {"error": "Invalid token: missing userId"}, 401

        return f(*args, **kwargs)
    return wrapper

def roles_required(*required_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not hasattr(g, "user_roles"):
                return {"error": "Missing authentication"}, 401

            if not any(role in g.user_roles for role in required_roles):
                return {"error": "Access forbidden: insufficient role"}, 403

            return f(*args, **kwargs)
        return wrapper
    return decorator