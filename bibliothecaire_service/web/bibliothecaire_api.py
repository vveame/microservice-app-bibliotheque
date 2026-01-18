from flask_restx import Namespace, Resource, fields
from flask import request
from service.bibliothecaire_service import BibliothecaireService
from dto.request_bibliothecaire_dto import RequestBibliothecaireDTO
from security.jwt_middleware import jwt_required, roles_required, admin_or_self

api = Namespace('bibliothecaires', description='Gestion des bibliothecaires')

service = BibliothecaireService()

# Define the expected input model for Swagger docs
bibliothecaire_model = api.model('BibliothecaireRequest', {
    'nom': fields.String(required=True, description='Nom de l\'bibliothecaire'),
    'prenom': fields.String(required=True, description='Prénom de l\'bibliothecaire'),
    'date_naissance': fields.String(required=True, description='Date de naissance'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password'),
    'role': fields.String(required=True, description='Role')
})

# Define output model (response) - you can customize fields shown
bibliothecaire_response_model = api.model('BibliothecaireResponse', {
    'id_bibliothecaire': fields.String(description='ID bibliothecaire'),
    'nom': fields.String(description='Nom de l\'bibliothecaire'),
    'prenom': fields.String(description='Prénom de l\'bibliothecaire'),
    'date_naissance': fields.String(description='Date de naissance'),
    'email': fields.String(description='Email'),
    'role': fields.String(description='Role'),
    'created_at': fields.DateTime(description='Date de creation'),
    'updated_at': fields.DateTime(description='Date de derniere modification')
})


@api.route('/')
class BibliothecaireList(Resource):
    @api.doc(security='Bearer')
    @jwt_required
    @roles_required('ROLE_ADMIN')
    @api.marshal_list_with(bibliothecaire_response_model)
    def get(self):
        """Récupérer tous les bibliothecaires"""
        return service.get_all_bibliothecaires()

    @api.doc(security='Bearer')
    @jwt_required
    @roles_required('ROLE_ADMIN')
    @api.expect(bibliothecaire_model)
    @api.marshal_with(bibliothecaire_response_model)
    def post(self):
        """Ajouter un bibliothecaire"""
        data = request.json
        dto = RequestBibliothecaireDTO(
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            date_naissance=data.get('date_naissance'),
            email=data.get('email'),
            password=data.get('password')
        )
        return service.add_bibliothecaire(dto)


@api.route('/<string:id>')
@api.param('id', 'Identifiant de l\'bibliothecaire')
class Bibliothecaire(Resource):
    @api.doc(security='Bearer')
    @jwt_required
    @admin_or_self(service)
    @api.marshal_with(bibliothecaire_response_model)
    def get(self, id):
        """Récupérer un bibliothecaire par ID"""
        return service.get_bibliothecaire_by_id(id)

    @api.doc(security='Bearer')
    @jwt_required
    @admin_or_self(service)
    @api.expect(bibliothecaire_model)
    @api.marshal_with(bibliothecaire_response_model)
    def put(self, id):
        """Modifier un bibliothecaire"""
        data = request.json
        dto = RequestBibliothecaireDTO(
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            date_naissance=data.get('date_naissance'),
            email=data.get('email'),
            password=data.get('password')
        )
        return service.update_bibliothecaire(id, dto)

    @api.doc(security='Bearer')
    @jwt_required
    @roles_required('ROLE_ADMIN')
    def delete(self, id):
        """Supprimer un bibliothecaire"""
        return service.delete_bibliothecaire(id)