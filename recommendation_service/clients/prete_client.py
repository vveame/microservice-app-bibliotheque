# clients/prete_client.py
import requests
from config import Config

PRETE_SERVICE_URL = f"{Config.PRETE_SERVICE_URL}/v1/pretes/lecteur/pretes"

def get_borrowed_books(reader_id, jwt_token: str):
    """
    Récupère les prêts réels d'un lecteur en passant le JWT pour l'authentification.
    """
    try:
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(f"{PRETE_SERVICE_URL}/{reader_id}", headers=headers)
        print("Prete service response status:", response.status_code)
        response.raise_for_status()
        prets = response.json()
        print("Borrowed books data:", prets)
        borrowed_books = [p["titre"] for p in prets]
        return borrowed_books
    except Exception as e:
        print("Error calling Prête service:", e)
        return []