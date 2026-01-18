class RequestBibliothecaireDTO:
    def __init__(
            self,
            nom=None,
            prenom=None,
            date_naissance=None,
            email=None,
            password=None
    ):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.email = email
        self.password = password

        # FORCE DEFAULT ROLE HERE
        self.role = "BIBLIOTHECAIRE"