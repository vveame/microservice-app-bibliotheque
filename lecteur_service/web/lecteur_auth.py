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
            "email": result["email"],
            "password": result["password"],  # hashed
            "role": "LECTEUR"
        }