from flask import request, g
from functools import wraps
import jwt
from config import Config
from flask_restx import abort

with open(Config.RSA_PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = f.read()

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", None)
        if not auth:
            return {"error": "Missing Authorization header"}, 401

        parts = auth.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return {"error": "Invalid Authorization header format"}, 401

        token = parts[1]
        try:
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"], options={"verify_aud": False}, leeway=30)
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}, 401
        except jwt.InvalidTokenError as e:
            return {"error": "Invalid token", "message": str(e)}, 401

        # Save user info and roles in Flask global context for use in the endpoint or other decorators
        g.user_email = payload.get("sub")
        # 'scope' claim is your roles string, space-separated
        g.user_roles = payload.get("scope", "").split()

        return f(*args, **kwargs)
    return wrapper

def roles_required(*required_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Make sure jwt_required ran before (g.user_roles should exist)
            if not hasattr(g, "user_roles"):
                return {"error": "Missing authentication"}, 401

            # Check if user has at least one required role
            if not any(role in g.user_roles for role in required_roles):
                return {"error": "Access forbidden: insufficient role"}, 403

            return f(*args, **kwargs)
        return wrapper
    return decorator

def admin_or_self(service, param_name="id"):
    """
    ROLE_ADMIN            full access
    ROLE_BIBLIOTHECAIRE   only own resource
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            roles = g.user_roles
            user_email = g.user_email

            # ADMIN: full access
            if "ROLE_ADMIN" in roles:
                return f(*args, **kwargs)

            # BIBLIOTHECAIRE: self-only
            if "ROLE_BIBLIOTHECAIRE" in roles:
                bibliothecaire_id = kwargs.get(param_name)
                bibliothecaire = service.get_bibliothecaire_by_id(bibliothecaire_id)

                if not bibliothecaire:
                    abort(404, "Bibliothécaire non trouvé")

                if bibliothecaire.email != user_email:
                    abort(403, "Accès interdit : uniquement votre propre compte")

                return f(*args, **kwargs)

            abort(403, "Accès interdit")
        return wrapper
    return decorator