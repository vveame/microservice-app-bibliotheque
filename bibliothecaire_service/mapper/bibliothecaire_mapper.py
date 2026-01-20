from dto.request_bibliothecaire_dto import RequestBibliothecaireDTO
from dto.response_bibliothecaire_dto import ResponseBibliothecaireDTO

class BibliothecaireMapper:
    def dto_to_entity(self, dto: RequestBibliothecaireDTO) -> dict:
        return {
            "nom": dto.nom,
            "prenom": dto.prenom,
            "date_naissance": dto.date_naissance,
            "email": dto.email,
            "password": dto.password,
            "role": dto.role
        }

    def entity_to_dto(self, entity: dict) -> ResponseBibliothecaireDTO:
        return ResponseBibliothecaireDTO(
            userId=str(entity.get("_id")),
            nom=entity.get("nom"),
            prenom=entity.get("prenom"),
            date_naissance=entity.get("date_naissance"),
            email=entity.get("email"),
            role=entity.get("role"),
            created_at = entity.get("created_at"),
            updated_at = entity.get("updated_at")
        )