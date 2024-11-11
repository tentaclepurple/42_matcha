# app/__init__.py

from flask import Flask
from .config.database import mongo, init_db
from .routes.user_endpoints import user_bp
from dotenv import load_dotenv
import os


load_dotenv()


def create_app():
    app = Flask(__name__)
    
    app.config["MONGO_URI"] = f"mongodb://{os.getenv('MONGO_ROOT_USERNAME')}:{os.getenv('MONGO_ROOT_PASSWORD')}@mongodb:27017/{os.getenv('MONGO_DATABASE')}?authSource=admin"
    
    mongo.init_app(app)
    
    with app.app_context():
        init_db()
    
    app.register_blueprint(user_bp)
    
    return app
