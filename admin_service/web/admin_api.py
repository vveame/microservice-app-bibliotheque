from flask_restx import Namespace, Resource, fields
from flask import request
from service.admin_service import AdminService
from dto.request_admin_dto import RequestAdminDTO
from security.jwt_middleware import jwt_required, roles_required

api = Namespace('admins', description='Gestion des admins')

service = AdminService()

# Define the expected input model for Swagger docs
admin_model = api.model('AdminRequest', {
    'nom': fields.String(required=True, description='Nom de l\'admin'),
    'prenom': fields.String(required=True, description='Prénom de l\'admin'),
    'date_naissance': fields.String(required=True, description='Date de naissance'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})

# Define output model (response) - you can customize fields shown
admin_response_model = api.model('AdminResponse', {
    'id_admin': fields.String(description='ID admin'),
    'nom': fields.String(description='Nom de l\'admin'),
    'prenom': fields.String(description='Prénom de l\'admin'),
    'date_naissance': fields.String(description='Date de naissance'),
    'email': fields.String(description='Email'),
    'role': fields.String(description='Role'),
    'created_at': fields.DateTime(description='Date de creation'),
    'updated_at': fields.DateTime(description='Date de derniere modification')
})

@api.route('/')
class AdminList(Resource):
    @api.doc(security='Bearer')
    @jwt_required
    @roles_required('ROLE_ADMIN')
    @api.marshal_list_with(admin_response_model)
    def get(self):
        """Récupérer tous les admins"""
        return service.get_all_admins()

    @api.doc(security='Bearer')
    @jwt_required
    @roles_required('ROLE_ADMIN')
    @api.expect(admin_model)
    @api.marshal_with(admin_response_model)
    def post(self):
        """Ajouter un admin"""
        data = request.json
        dto = RequestAdminDTO(
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            date_naissance=data.get('date_naissance'),
            email=data.get('email'),
            password=data.get('password')
        )
        return service.add_admin(dto)


@api.route('/<string:id>')
@api.param('id', 'Identifiant de l\'admin')
class Admin(Resource):
    @api.doc(security='Bearer')
    @jwt_required
    @roles_required('ROLE_ADMIN')
    @api.marshal_with(admin_response_model)
    def get(self, id):
        """Récupérer un admin par ID"""
        return service.get_admin_by_id(id)

    @api.doc(security='Bearer')
    @jwt_required
    @roles_required('ROLE_ADMIN')
    @api.expect(admin_model)
    @api.marshal_with(admin_response_model)
    def put(self, id):
        """Modifier un admin"""
        data = request.json
        dto = RequestAdminDTO(
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            date_naissance=data.get('date_naissance'),
            email=data.get('email'),
            password=data.get('password')
        )
        return service.update_admin(id, dto)

    @api.doc(security='Bearer')
    @jwt_required
    @roles_required('ROLE_ADMIN')
    def delete(self, id):
        """Supprimer un admin"""
        return service.delete_admin(id)