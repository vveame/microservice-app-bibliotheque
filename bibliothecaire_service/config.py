import os

class Config:
    # Database
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo-db:27017/bibliothecaire_db")

    APP_NAME = os.getenv("APP_NAME", "BIBLIOTHECAIRE-SERVICE")
    APP_PORT = int(os.getenv("APP_PORT", "8082"))

    # Security
    INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")

    # Eureka
    EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://discovery-service:8761/eureka")

    # JWT public key path
    RSA_PUBLIC_KEY_PATH = os.getenv("RSA_PUBLIC_KEY_PATH", "keys/publicKey.pem")
