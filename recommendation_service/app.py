from flask import Flask, jsonify, g
from recommender import BookRecommender
from clients.prete_client import get_borrowed_books
from clients.livre_client import fetch_books
from config import Config
from security.jwt_middleware import jwt_required, roles_required

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/recommend", methods=["GET"])
    @jwt_required
    @roles_required("ROLE_LECTEUR")
    def recommend_books():
        """
        Retourne les recommandations pour l'utilisateur connecté.
        Nettoie les titres empruntés avant de passer au recommendeur.
        """
        user_id = g.userId
        jwt_token = g.jwt_token  # token pour appel interne au service Prêt

        # Récupérer le catalogue complet de livres
        books_df = fetch_books()
        recommender = BookRecommender(books_df)

        # Récupérer les livres empruntés
        borrowed_books = get_borrowed_books(user_id, jwt_token)

        # nettoyer les titres
        cleaned_borrowed_books = [t.replace("Demande du livre ", "").strip() for t in borrowed_books]

        # Générer les recommandations
        recommendations = recommender.recommend(cleaned_borrowed_books)

        return jsonify({
            "reader_id": user_id,
            "borrowed_books": cleaned_borrowed_books,
            "recommendations": recommendations
        })

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "UP"}), 200

    return app

if __name__ == "__main__":
    from eureka_client import start_eureka_client
    start_eureka_client()
    app = create_app()
    app.run(host="0.0.0.0", port=Config.APP_PORT)