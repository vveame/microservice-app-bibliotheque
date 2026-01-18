from dto.request_admin_dto import RequestAdminDTO
from dto.response_admin_dto import ResponseAdminDTO

class AdminMapper:
    def dto_to_entity(self, dto: RequestAdminDTO) -> dict:
        return {
            "nom": dto.nom,
            "prenom": dto.prenom,
            "date_naissance": dto.date_naissance,
            "email": dto.email,
            "password": dto.password,
            "role": dto.role,
        }

    def entity_to_dto(self, entity: dict) -> ResponseAdminDTO:
        return ResponseAdminDTO(
            id_admin=str(entity.get("_id")),
            nom=entity.get("nom"),
            prenom=entity.get("prenom"),
            date_naissance=entity.get("date_naissance"),
            email=entity.get("email"),
            role=entity.get("role"),
            created_at = entity.get("created_at"),
            updated_at = entity.get("updated_at")
        )