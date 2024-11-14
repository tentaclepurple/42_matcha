# app/__init__.py

from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta

from .config.database import mongo, init_db
from .routes.user_endpoints import user_bp

from dotenv import load_dotenv
import os


load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=10)
    
    
    app.config["MONGO_URI"] = (
    f"mongodb://{os.getenv('MONGO_ROOT_USERNAME')}:"
    f"{os.getenv('MONGO_ROOT_PASSWORD')}@mongodb:27017/"
    f"{os.getenv('MONGO_DATABASE')}?authSource=admin"
)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')


    mongo.init_app(app)
    jwt = JWTManager(app)
    
    # Registrar blueprints
    app.register_blueprint(user_bp, url_prefix='/api/users')

    with app.app_context():
        init_db()
        
    return app
