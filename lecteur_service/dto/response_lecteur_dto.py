class ResponseLecteurDTO:
    def __init__(
            self,
            userId=None,
            nom=None,
            prenom=None,
            date_naissance=None,
            email=None,
            role= None,
            created_at=None,
            updated_at=None
    ):
        self.userId = userId
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.email = email
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at