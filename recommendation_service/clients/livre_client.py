import requests
import pandas as pd
from config import Config

LIVRE_SERVICE_URL = f"{Config.LIVRE_SERVICE_URL}/v1/livres"

def fetch_books():
    try:
        response = requests.get(LIVRE_SERVICE_URL)
        print("Livre service response status:", response.status_code)
        response.raise_for_status()
        books = response.json()
        print("Fetched books:", books)
        df = pd.DataFrame(books)
        return df
    except Exception as e:
        print("Error calling Livre service:", e)
        return pd.DataFrame()
