# app/routes/user_endpoints.py

import jwt
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_jwt
    )
from werkzeug.security import (
    generate_password_hash, check_password_hash
    )

from ..models.user import UserModel
from ..utils.email import send_verification_email
from ..utils.decorators import login_required
from ..config.redis import redis_client

from datetime import datetime, timedelta


user_bp = Blueprint('user', __name__)

DEFAULT = "static/default/default.png"

@user_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        existing_user = UserModel.find_by_username(data['username'])
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 409

        existing_email = UserModel.find_by_email(data['email'])
        if existing_email:
            print("Email already exists but its ok for develpment")
            #return jsonify({'error': 'Email already exists'}), 409
        
        # Verify required fields
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing field: {field}'}), 400

        user = {
            # Required
            "username": data["username"],
            "email": data["email"],
            "password": generate_password_hash(data["password"]),
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "verified": False,
            "created_at": datetime.utcnow(),
            
            # Status
            "online": False,
            "last_connection": datetime.utcnow(),
            "profile_completed": False,
            
            # Profile
            "gender": None,
            "sexual_preferences": None,
            "biography": "",
            "interests": [],
            "photos": [
                {'url': DEFAULT, 'is_profile': i==0, 'uploaded_at': datetime.utcnow()}
                for i in range(5)
            ],
            "location": None,
            "fame_rating": 0,
            
            # Other
            "blocked_users": [],
            "reported": False
        }
        
        # Insert user into database
        user_id = UserModel.create_user(user)
        
        # generate verification token
        token = jwt.encode(
            {
                'user_id': str(user_id),
                'exp': datetime.utcnow() + timedelta(hours=24)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        # send verification email
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
        # decode token
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        
        # update user verified status
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


@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Check required fields
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
            
        # Find user and check credentials
        user = UserModel.find_by_username(data['username'])
        if not user or not check_password_hash(user['password'], data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
            
        # Check verification
        if not user['verified']:
            return jsonify({'error': 'Email not verified'}), 401

        # Generate access token
        access_token = create_access_token(identity=str(user['_id']))

        # Update online status
        UserModel.update_online_status(str(user['_id']), True)
        
        # Generate response
        user_data = {
            'user_id': str(user['_id']),
            'profile_completed': user['profile_completed']
        }
        
        # WE CAN ADD MORE USER DATA TO THE RESPONSE IF NEEDED
        # CAUTION WITH NON SERIALIZABLE DATA TYPES LIKE DATETIME, GEOJSON, ETC.
        # response['user_data'] = user
        
        return jsonify({
            'access_token': access_token,
            'user': user_data
            }),200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # Obtener identificador único del token
        jti = get_jwt()["jti"]
        current_user_id = get_jwt_identity()
        
        # Añadir a lista negra en Redis
        # Usamos el tiempo de expiración del token
        redis_client.set(
            f"token_blacklist:{jti}",
            str(datetime.utcnow()),
            ex=3600  # 1 hora o el tiempo que configures para los tokens
        )
        
        # Actualizar estado online
        UserModel.update_online_status(current_user_id, False)
        
        return jsonify({'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500