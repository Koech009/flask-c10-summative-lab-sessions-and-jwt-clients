from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate, jwt, bcrypt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import models
    from server import models

    # Register blueprints
    from server.routes.auth_routes import auth_bp
    from server.routes.workout_routes import workouts_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(workouts_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(400)
    def bad_request(error):
        return {"error": "Bad request"}, 400

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5555, debug=True)
