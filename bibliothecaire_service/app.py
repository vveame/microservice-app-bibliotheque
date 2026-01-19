from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify
from config import Config
from extensions import mongo
from flask_restx import Api
from global_error_handler import register_error_handlers
from prometheus_metrics import setup_metrics

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    setup_metrics(app)

    # Initialize PyMongo
    mongo.init_app(app)
    with app.app_context():
        mongo.db.bibliothecaires.create_index(
            "email",
            unique=True
        )

    # Create RESTX API and register namespace
    from web.bibliothecaire_api import api as bibliothecaire_ns
    from web.bibliothecaire_auth import api as bibliothecaire_auth_ns

    api = Api(app, version='1.0', title=Config.APP_NAME, description='API de gestion des bibliothecaires', doc='/swagger/')

    # Public API (JWT protected)
    api.add_namespace(bibliothecaire_ns, path='/v1/bibliothecaires')

    # Internal auth API (API-key protected)
    api.add_namespace(bibliothecaire_auth_ns, path='/internal')

    # simple root and health endpoints

    @app.route("/actuator/health")
    def health():
        return jsonify({"status": "UP"})

    register_error_handlers(api)

    return app


if __name__ == "__main__":
    from eureka_client import start_eureka_client
    start_eureka_client()
    app = create_app()
    app.run(host="0.0.0.0", port=Config.APP_PORT)
