# app/routes/user_endpoints.py


from flask import Blueprint, request, jsonify, current_app
from ..models.user import UserModel
from ..utils.email import send_verification_email
from werkzeug.security import generate_password_hash
import jwt
from datetime import datetime, timedelta


user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Verificar campos requeridos
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Crear usuario con verified=False
        user = {
            "username": data["username"],
            "email": data["email"],
            "password": generate_password_hash(data["password"]),
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "verified": False,
            "created_at": datetime.utcnow()
        }
        
        # Insertar usuario
        user_id = UserModel.create_user(user)
        
        # Generar token de verificación

        token = jwt.encode(
            {
                'user_id': str(user_id),
                'exp': datetime.utcnow() + timedelta(hours=24)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        # Enviar email de verificación
        send_verification_email(data["email"], token)
        
        return jsonify({
            "message": "User registered successfully. "
            "Please check your email to verify your account.",
            "user_id": user_id
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        # Decodificar token
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        
        # Actualizar usuario como verificado
        UserModel.verify_user(payload['user_id'])
        
        return jsonify({
            "message": "Email verified successfully"
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Verification link has expired"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid verification token"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
