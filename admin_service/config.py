import os

class Config:
    # Database
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/admin_db")

    APP_NAME = os.getenv("APP_NAME", "ADMIN-SERVICE")
    APP_PORT = int(os.getenv("APP_PORT", "8084"))

    #Security
    INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")
    DEFAULT_ADMIN_EMAIL= os.getenv("DEFAULT_ADMIN_EMAIL")
    DEFAULT_ADMIN_PASSWORD= os.getenv("DEFAULT_ADMIN_PASSWORD")
    FORCE_PASSWORD_CHANGE= os.getenv("FORCE_PASSWORD_CHANGE")

    # Eureka
    EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka")

    # JWT public key path
    RSA_PUBLIC_KEY_PATH = os.getenv("RSA_PUBLIC_KEY_PATH", "keys/publicKey.pem")
