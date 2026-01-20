import os

class Config:

    APP_NAME = os.getenv("APP_NAME", "RECOMMENDATION-SERVICE")
    APP_PORT = int(os.getenv("APP_PORT", "8085"))

    LIVRE_SERVICE_URL = os.getenv(
        "LIVRE_SERVICE_URL",
        "http://livre-service:8080"
    )

    PRETE_SERVICE_URL = os.getenv(
        "PRETE_SERVICE_URL",
        "http://prete-service:8081"
    )

    # Eureka
    EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://discovery-service:8761/eureka")

    RSA_PUBLIC_KEY_PATH = os.getenv("RSA_PUBLIC_KEY_PATH", "keys/publicKey.pem")

