from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

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

    # CLI commands to prove SQLAlchemy + CLI usage
    @app.cli.command("db_create")
    def db_create():
        with app.app_context():
            db.create_all()
            print("Database tables created")

    @app.cli.command("db_drop")
    def db_drop():
        with app.app_context():
            db.drop_all()
            print("Database tables dropped")

    @app.cli.command("seed")
    def seed_command():
        from seed import seed_data
        seed_data(app)
        print("Database seeded")

    return app
