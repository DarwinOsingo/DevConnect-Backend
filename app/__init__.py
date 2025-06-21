from flask import Flask
from app.extensions import db, migrate, bcrypt
from app.middleware.cors_middleware import init_cors  # ✅ Add this

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    #  Initialize CORS
    init_cors(app)

    # Register blueprints
    from app.api.auth import auth_bp
    from app.api.users import users_bp
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')

    return app
