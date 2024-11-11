# app/models/user.py

from ..config.database import mongo
from datetime import datetime


""" class UserModel:
    @staticmethod
    def create_user(user_data):
        existing_user = mongo.db.users.find_one({
            "$or": [
                {"username": user_data["username"]},
                {"email": user_data["email"]}
            ]
        })
        
        if existing_user:
            raise ValueError(f"User with username {user_data['username']} or email {user_data['email']} already exists")
            
        result = mongo.db.users.insert_one(user_data)
        return str(result.inserted_id) """


from ..config.database import mongo
from bson import ObjectId
from datetime import datetime

class UserModel:
    @staticmethod
    def create_user(user_data):
        """Crear un nuevo usuario"""
        # Verificar si existe
        existing_user = mongo.db.users.find_one({
            "$or": [
                {"username": user_data["username"]},
                {"email": user_data["email"]}
            ]
        })
        
        if existing_user:
            raise ValueError(f"User with username {user_data['username']} or email {user_data['email']} already exists")
            
        result = mongo.db.users.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def update_online_status(user_id: str, is_online: bool):
        """Actualizar estado online y última conexión"""
        return mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "online": is_online,
                    "last_connection": datetime.utcnow()
                }
            }
        )

    @staticmethod
    def update_profile(user_id: str, profile_data: dict):
        """Actualizar datos del perfil"""
        return mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": profile_data}
        )

    @staticmethod
    def find_by_id(user_id: str):
        """Buscar usuario por ID"""
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def find_by_username(username: str):
        """Buscar usuario por username"""
        return mongo.db.users.find_one({"username": username})
