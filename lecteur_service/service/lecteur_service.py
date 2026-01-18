# service/lecteur_service.py

from dto.request_lecteur_dto import RequestLecteurDTO
from mapper.lecteur_mapper import LecteurMapper
from repository.lecteur_repository import LecteurRepository
from security.password_utils import hash_password, verify_password
from .exception_service import NotFoundException, ConflictException, BadRequestException
from pymongo.errors import DuplicateKeyError

class LecteurService:
    def __init__(self):
        self.repo = LecteurRepository()
        self.mapper = LecteurMapper()

    def add_lecteur(self, dto: RequestLecteurDTO):
        if not dto.email or not dto.password:
            raise BadRequestException("Email et mot de passe sont obligatoires")

        try:
            dto.password = hash_password(dto.password)
            entity = self.mapper.dto_to_entity(dto)
            saved_entity = self.repo.save(entity)
            return self.mapper.entity_to_dto(saved_entity)

        except DuplicateKeyError:
            raise ConflictException("Un lecteur avec cet email existe déjà")

    def get_all_lecteurs(self):
        entities = self.repo.find_all()
        return [self.mapper.entity_to_dto(e) for e in entities]

    def get_lecteur_by_id(self, id):
        entity = self.repo.find_by_id(id)
        if not entity:
            raise NotFoundException("Lecteur non trouvé")
        return self.mapper.entity_to_dto(entity)

    def _get_lecteur_by_email(self, email):
        return self.repo.find_by_email(email)

    def update_lecteur(self, id, dto: RequestLecteurDTO):
        entity = self.repo.find_by_id(id)
        if not entity:
            raise NotFoundException("Lecteur non trouvé")

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

    def delete_lecteur(self, id):
        if not self.repo.delete(id):
            raise NotFoundException("Lecteur non trouvé")