# service/admin_service.py

from dto.request_admin_dto import RequestAdminDTO
from mapper.admin_mapper import AdminMapper
from repository.admin_repository import AdminRepository
from security.password_utils import hash_password, verify_password
from .exception_service import NotFoundException, ConflictException, BadRequestException
from pymongo.errors import DuplicateKeyError

class AdminService:
    def __init__(self):
        self.repo = AdminRepository()
        self.mapper = AdminMapper()

    def add_admin(self, dto: RequestAdminDTO):
        if not dto.email or not dto.password:
            raise BadRequestException("Email et mot de passe sont obligatoires")

        try:
            dto.password = hash_password(dto.password)
            entity = self.mapper.dto_to_entity(dto)
            saved_entity = self.repo.save(entity)
            return self.mapper.entity_to_dto(saved_entity)
        except DuplicateKeyError:
            raise ConflictException("Un admin avec cet email existe déjà")

    def get_all_admins(self):
        entities = self.repo.find_all()
        return [self.mapper.entity_to_dto(e) for e in entities]

    def get_admin_by_id(self, id):
        entity = self.repo.find_by_id(id)
        if not entity:
            raise NotFoundException("Admin non trouvé")
        return self.mapper.entity_to_dto(entity)

    def _get_admin_by_email(self, email):
        return self.repo.find_by_email(email)

    def update_admin(self, id, dto: RequestAdminDTO):
        entity = self.repo.find_by_id(id)
        if not entity:
            raise NotFoundException("Admin non trouvé")

        update_data = {}
        if dto.nom is not None:
            update_data["nom"] = dto.nom
        if dto.prenom is not None:
            update_data["prenom"] = dto.prenom
        if dto.date_naissance is not None:
            update_data["date_naissance"] = dto.date_naissance
        if dto.email is not None:
            update_data["email"] = dto.email

        # Only hash if password is provided AND not empty
        if dto.password and dto.password.strip():
            update_data["password"] = hash_password(dto.password)

        if not update_data:
            raise BadRequestException("Aucune donnée valide à mettre à jour")

        updated_entity = self.repo.update(id, update_data)
        if not updated_entity:
            return None
        return self.mapper.entity_to_dto(updated_entity)

    def delete_admin(self, id):
        if not self.repo.delete(id):
            raise NotFoundException("Admin non trouvé")