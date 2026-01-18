from service.exception_service import ServiceException

def register_error_handlers(api):

    @api.errorhandler(ServiceException)
    def handle_service_exception(e):
        return {
            "error": e.message
        }, e.status_code

    @api.errorhandler(Exception)
    def handle_generic_exception(e):
        return {
            "error": "Erreur interne du serveur"
        }, 500
