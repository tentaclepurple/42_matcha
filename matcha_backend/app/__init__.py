# app/__init__.py

from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta

from .config.database import mongo, init_db
from .routes.user_endpoints import user_bp
from .routes.profile_endpoints import profile_bp
from .routes.tag_endpoints import tags_bp
from .routes.interaction_endpoints import interaction_bp
from .routes.match_endpoints import match_bp
from .routes.notification_endpoints import notification_bp
from .routes.chat_endpoints import chat_bp
from .models.iamatcha import BotModel
from .scripts.generate_test_users import generate_test_users

from dotenv import load_dotenv
import os


load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=40)

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

    with app.app_context():
        init_db()

    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    app.register_blueprint(tags_bp, url_prefix='/api/tags')
    app.register_blueprint(interaction_bp, url_prefix='/api/interactions')
    app.register_blueprint(match_bp, url_prefix='/api/match')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')

    num_users = mongo.db.users.count_documents({})
    num_test_users = 500
    if (num_users < num_test_users):
        generate_test_users(mongo, num_test_users - num_users)

    BotModel.check_and_create_bot()

    return app
