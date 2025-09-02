from flask import Flask, jsonify
from config import Config
from db import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from routes import api
    from routes.users import users_bp
    from routes.spots import spots_bp
    from routes.reservations import reservations_bp

    app.register_blueprint(api)
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(spots_bp, url_prefix="/spots")
    app.register_blueprint(reservations_bp, url_prefix="/reservations")

    # JSON error handlers
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(400)
    def handle_400(error):
        return jsonify({"error": "Bad request"}), 400

    # Keep app-only CLI; dedicated CLI in cli.py

    return app
