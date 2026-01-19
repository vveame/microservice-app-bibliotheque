from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify
from config import Config
from extensions import mongo
from flask_restx import Api
from service.admin_initializer import AdminInitializer
from global_error_handler import register_error_handlers
from prometheus_metrics import setup_metrics

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup Prometheus monitoring
    setup_metrics(app)

    # Initialize PyMongo
    mongo.init_app(app)
    with app.app_context():
        mongo.db.admins.create_index(
            "email",
            unique=True
        )
        # Initialize default admin user
        try:
            initializer = AdminInitializer()
            initializer.create_default_admin()
        except Exception as e:
            print(f"Warning: Could not create default admin: {e}")

    # Create RESTX API and register namespace
    from web.admin_api import api as admin_ns
    from web.admin_auth import api as admin_auth_ns
    api = Api(app, version='1.0', title=Config.APP_NAME, description='API de gestion des admins', doc='/swagger/')
    api.add_namespace(admin_ns, path='/v1/admins')
    api.add_namespace(admin_auth_ns, path='/internal')

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
