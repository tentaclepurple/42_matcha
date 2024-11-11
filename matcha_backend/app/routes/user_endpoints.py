# app/routes/user_endpoints.py

from flask import Blueprint, request
from ..models.user import UserModel
from datetime import datetime

user_bp = Blueprint('user', __name__)


""" @user_bp.route('/populate')
def populate_db():
    try:
        user = {
            "username": "test_user",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "test123",  # Debería estar hasheada
            "verified": False,
            "created_at": datetime.utcnow(),
            "online": False,
            "last_connection": datetime.utcnow(),
            "profile": {
                "completed": False,
                "gender": "male",
                "sexual_preferences": ["female"],
                "biography": "Test bio",
                "interests": ["sports", "music"],
                "photos": [
                    {
                        "url": "/uploads/photo1.jpg",
                        "is_profile": True,
                        "uploaded_at": datetime.utcnow()
                    }
                ],
                "location": {
                    "type": "Point",
                    "coordinates": [-3.7037902, 40.4167754]  # Madrid
                },
                "fame_rating": 0
            },
            "blocked_users": []
        }
        
        user_id = UserModel.create_user(user)
        
        return {
            "message": "User created successfully",
            "user_id": user_id
        }, 201
            
    except ValueError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": str(e)}, 500 """


# app/routes/user_endpoints.py
from flask import Blueprint, request, jsonify
from ..models.user import UserModel
from datetime import datetime
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    try:
        # Obtener datos del request
        data = request.get_json()
        
        # Verificar campos requeridos
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "error": f"Missing required field: {field}"
                }), 400

        # Crear usuario con campos obligatorios
        user = {
            "username": data["username"],
            "email": data["email"],
            "password": generate_password_hash(data["password"]),  # Hashear password
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "verified": False,  # Requiere verificación por email
            "created_at": datetime.utcnow(),
            "online": True,
            "last_connection": datetime.utcnow(),
            "profile_completed": False,
            "fame_rating": 0
        }
        
        user_id = UserModel.create_user(user)
        
        # TODO: Enviar email de verificación
        
        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id
        }), 201
            
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500