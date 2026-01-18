class ServiceException(Exception):
    status_code = 400
    message = "Erreur métier"

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)


class NotFoundException(ServiceException):
    status_code = 404
    message = "Ressource introuvable"


class ConflictException(ServiceException):
    status_code = 409
    message = "Conflit de données"


class BadRequestException(ServiceException):
    status_code = 400
    message = "Requête invalide"