# clients/livre_client.py
import requests
from config import Config

LIVRE_SERVICE_URL = f"{Config.LIVRE_SERVICE_URL}/v1/livres"

def fetch_books():
    """
    Récupère tous les livres pour la recommandation.
    """
    try:
        response = requests.get(LIVRE_SERVICE_URL)
        response.raise_for_status()
        livres = response.json()
        import pandas as pd
        return pd.DataFrame(livres)
    except Exception as e:
        print("Error fetching books:", e)
        return pd.DataFrame()  # DataFrame vide si erreur
