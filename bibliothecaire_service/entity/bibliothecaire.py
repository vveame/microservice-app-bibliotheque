# MongoDB doesn’t need a model class
# entity is a dict

def make_bibliothecaire_dict(nom, prenom, date_naissance, email, password, created_date, updated_date):
    return {
        "nom": nom,
        "prenom": prenom,
        "date_naissance": date_naissance,
        "email": email,
        "password": password,
        "role": "BIBLIOTHECAIRE",
        "created_at": created_date,
        "updated_at": updated_date
    }