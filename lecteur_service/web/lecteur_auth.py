from config import Config
from flask import request, abort
from flask_restx import Namespace, Resource
from service.lecteur_service import LecteurService

api = Namespace('internal', description='Authentication des lecteurs')

service = LecteurService()

@api.route('/email/<string:email>')
class LecteurByEmail(Resource):
    def get(self, email):
        api_key = request.headers.get("X-API-KEY")

        if not api_key or api_key != Config.INTERNAL_API_KEY:
            abort(403, "Forbidden: internal access only")

        result = service._get_lecteur_by_email(email)
        if not result:
            abort(404, "Lecteur non trouvé")

        return {
            "userId": result.get("userId") or str(result.get("_id")),
            "email": result["email"],
            "password": result["password"],  # hashed
            "role": "LECTEUR"
        }

@api.route('/lecteurs/<string:id>')
class LecteurInternal(Resource):
    def get(self, id):
        api_key = request.headers.get("X-API-KEY")

        # Check internal API key for security
        if not api_key or api_key != Config.INTERNAL_API_KEY:
            abort(403, "Forbidden: internal access only")

        lecteur_dto = service.get_lecteur_by_id(id)
        if not lecteur_dto:
            abort(404, "Lecteur non trouvé")

        def serialize_date(dt):
            return dt.isoformat() if dt else None

        return {
            "userId": lecteur_dto.userId,
            "nom": getattr(lecteur_dto, "nom", None),
            "prenom": getattr(lecteur_dto, "prenom", None),
            "date_naissance": getattr(lecteur_dto, "date_naissance", None),
            "email": getattr(lecteur_dto, "email", None),
            "password": getattr(lecteur_dto, "password", None),
            "role": getattr(lecteur_dto, "role", None),
            "created_at": serialize_date(getattr(lecteur_dto, "created_at", None)),
            "updated_at": serialize_date(getattr(lecteur_dto, "updated_at", None)),
        }