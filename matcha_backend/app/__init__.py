# app/__init__.py
from flask import Flask, request
from flask_pymongo import PyMongo
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
mongo = PyMongo()

def init_db():
    """Crear colección con su estructura al iniciar el servidor"""
    try:
        # Crear la colección con validación
        mongo.db.create_collection("users", 
            validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["username", "email", "password", "created_at"],
                    "properties": {
                        "_id": {
                            "bsonType": "objectId",
                            "description": "must be an ObjectId and is automatically generated"
                        },
                        "username": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "email": {
                            "bsonType": "string",
                            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                            "description": "must be a valid email address"
                        },
                        "password": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "created_at": {
                            "bsonType": "date",
                            "description": "must be a date and is required"
                        },
                        "profile_completed": {
                            "bsonType": "bool",
                            "description": "must be a boolean"
                        }
                    },
                    "additionalProperties": False
                }
            }
        )
        # Crear índices únicos
        mongo.db.users.create_index("username", unique=True)
        mongo.db.users.create_index("email", unique=True)
        print("Database initialized successfully")
    except Exception as e:
        # Si la colección ya existe, ignoramos el error
        if "already exists" not in str(e):
            print(f"Error initializing database: {e}")


def create_app():
    app = Flask(__name__)
    

    # Configuración usando variables de entorno
    app.config["MONGO_URI"] = f"mongodb://{os.getenv('MONGO_ROOT_USERNAME')}:{os.getenv('MONGO_ROOT_PASSWORD')}@mongodb:27017/{os.getenv('MONGO_DATABASE')}?authSource=admin"
    
    # Inicializar MongoDB
    mongo.init_app(app)
    
    # Inicializar la base de datos al arrancar
    with app.app_context():
        init_db()
    
    @app.route('/populate')
    def populate_db():
        try:
            user = {
                "username": "jui",
                "email": "efwt@test.com",
                "password": "test123",
                "created_at": datetime.utcnow(),
                "profile_completed": False,
            }
            
            # Verificar si existe
            existing_user = mongo.db.users.find_one({
                "$or": [
                    {"username": user["username"]},
                    {"email": user["email"]}
                ]
            })
            
            if existing_user:
                return {
                    "error": f"User with username {user['username']} or email {user['email']} already exists"
                }, 400
                
            # Insertar usuario
            result = mongo.db.users.insert_one(user)
            
            return {
                "message": "User created successfully",
                "user_id": str(result.inserted_id)
            }, 201
                
        except Exception as e:
            return {"error": str(e)}, 500
    
    return app


""" from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config["MONGO_URI"] = "mongodb://root:rootpassword@mongodb:27017/matcha?authSource=admin"
    
    # Inicializar MongoDB
    mongo.init_app(app)
    
    @app.route('/init-db')
    def init_db():
        # Crear dos usuarios de prueba
        users = [
            {
                "username": "user1",
                "email": "user1@test.com",
                "age": 25
            },
            {
                "username": "user2",
                "email": "user2@test.com",
                "age": 30
            }
        ]
        
        # Insertar usuarios
        mongo.db.users.insert_many(users)
        
        return {"message": "Database initialized with test users"}
    
    return app """