from flask_restx import Namespace, Resource, fields
from flask import request
from service.lecteur_service import LecteurService
from dto.request_lecteur_dto import RequestLecteurDTO
from security.jwt_middleware import jwt_required, roles_required, admin_biblio_or_self, admin_or_self

api = Namespace('lecteurs', description='Gestion des lecteurs')

service = LecteurService()

# Define the expected input model for Swagger docs
lecteur_model = api.model('LecteurRequest', {
    'nom': fields.String(required=True, description='Nom de l\'lecteur'),
    'prenom': fields.String(required=True, description='Prénom de l\'lecteur'),
    'date_naissance': fields.String(required=True, description='Date de naissance'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password'),
    'role': fields.String(required=True, description='Role')
})

# Define output model (response) - you can customize fields shown
lecteur_response_model = api.model('LecteurResponse', {
    'id_lecteur': fields.String(description='ID lecteur'),
    'nom': fields.String(description='Nom de l\'lecteur'),
    'prenom': fields.String(description='Prénom de l\'lecteur'),
    'date_naissance': fields.String(description='Date de naissance'),
    'email': fields.String(description='Email'),
    'role': fields.String(description='Role'),
    'created_at': fields.DateTime(description='Date de creation'),
    'updated_at': fields.DateTime(description='Date de derniere modification')
})


@api.route('/')
class LecteurList(Resource):
    @api.doc(security='Bearer')
    @jwt_required
    @roles_required('ROLE_BIBLIOTHECAIRE', 'ROLE_ADMIN')
    @api.marshal_list_with(lecteur_response_model)
    def get(self):
        """Récupérer tous les lecteurs"""
        return service.get_all_lecteurs()

    @api.doc(security='Bearer')
    @jwt_required
    @roles_required('ROLE_ADMIN')
    @api.expect(lecteur_model)
    @api.marshal_with(lecteur_response_model)
    def post(self):
        """Ajouter un lecteur"""
        data = request.json
        dto = RequestLecteurDTO(
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            date_naissance=data.get('date_naissance'),
            email=data.get('email'),
            password=data.get('password')
        )
        return service.add_lecteur(dto)


@api.route('/<string:id>')
@api.param('id', 'Identifiant de l\'lecteur')
class Lecteur(Resource):
    @api.doc(security='Bearer')
    @jwt_required
    @admin_biblio_or_self(service)
    @api.marshal_with(lecteur_response_model)
    def get(self, id):
        """Récupérer un lecteur par ID"""
        return service.get_lecteur_by_id(id)

    @api.doc(security='Bearer')
    @jwt_required
    @admin_or_self(service)
    @api.expect(lecteur_model)
    @api.marshal_with(lecteur_response_model)
    def put(self, id):
        """Modifier un lecteur"""
        data = request.json
        dto = RequestLecteurDTO(
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            date_naissance=data.get('date_naissance'),
            email=data.get('email'),
            password=data.get('password')
        )
        return service.update_lecteur(id, dto)

    @api.doc(security='Bearer')
    @jwt_required
    @roles_required('ROLE_ADMIN')
    def delete(self, id):
        """Supprimer un lecteur"""
        return service.delete_lecteur(id)