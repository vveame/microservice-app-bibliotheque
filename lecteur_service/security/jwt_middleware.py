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

def admin_biblio_or_self(service, id_param="id"):
    """
    ROLE_ADMIN             full access
    ROLE_BIBLIOTHECAIRE    full access
    ROLE_LECTEUR           only own resource
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            roles = g.user_roles
            user_email = g.user_email

            # ADMIN & BIBLIOTHECAIRE: full access
            if "ROLE_ADMIN" in roles or "ROLE_BIBLIOTHECAIRE" in roles:
                return f(*args, **kwargs)

            # LECTEUR: self-only
            if "ROLE_LECTEUR" in roles:
                lecteur_id = kwargs.get(id_param)
                lecteur = service.get_lecteur_by_id(lecteur_id)

                if not lecteur:
                    abort(404, "Lecteur non trouvé")

                if lecteur.email != user_email:
                    abort(403, "Accès interdit : uniquement votre propre compte")

                return f(*args, **kwargs)

            abort(403, "Accès interdit")
        return wrapper
    return decorator

def admin_or_self(service, id_param="id"):
    """
    ROLE_ADMIN: full access
    ROLE_LECTEUR: only own resource
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            roles = g.user_roles
            user_email = g.user_email

            # ADMIN: full access
            if "ROLE_ADMIN" in roles:
                return f(*args, **kwargs)

            # LECTEUR: self-only access
            if "ROLE_LECTEUR" in roles:
                lecteur_id = kwargs.get(id_param)
                lecteur = service.get_lecteur_by_id(lecteur_id)

                if not lecteur:
                    abort(404, "Lecteur non trouvé")

                if lecteur.email != user_email:
                    abort(403, "Accès interdit : uniquement votre propre compte")

                return f(*args, **kwargs)

            # If role is neither ADMIN nor LECTEUR, forbid access
            abort(403, "Accès interdit")
        return wrapper
    return decorator