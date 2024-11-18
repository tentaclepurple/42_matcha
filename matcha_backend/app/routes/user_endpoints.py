# app/routes/user_endpoints.py

import jwt
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_jwt)
from werkzeug.security import (
    generate_password_hash, check_password_hash)
from ..models.user import UserModel
from ..utils.email import send_verification_email, send_reset_password_email
from ..utils.services import get_location_by_ip, get_public_ip
from ..utils.validators import validate_username, validate_password
from ..config.redis import redis_client
from datetime import datetime, timedelta
import requests


user_bp = Blueprint('user', __name__)

DEFAULT = "static/default/default.png"

@user_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # Validate username
        is_valid, error_msg = validate_username(data.get('username', ''))
        if not is_valid:
            return jsonify({'error': error_msg}), 400
            
        # Validate password
        is_valid, error_msg = validate_password(data.get('password', ''))
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        existing_user = UserModel.find_by_username(data['username'])
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 409

        existing_email = UserModel.find_by_email(data['email'])
        if existing_email:
            print("Email already exists")
            #return jsonify({'error': 'Email already exists'}), 409 # Comment this line for DEVELOPMENT
        
        # Verify required fields
        required_fields = [
            'username', 'email', 'password', 'first_name', 'last_name', 'age'
            ]
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing field: {field}'}), 400
        try:
            age = int(data['age'])
            if age < 18:
                return jsonify({'error': 'Must be 18 or older'}), 400
        except ValueError:
            return jsonify({'error': 'Age must be a number'}), 400
        
        location = data.get('location')
        # if location doesn't come from the frontend, get it from the IP
        if not location:
            # If no location provided, get it from IP
            publicip = get_public_ip()
            location = get_location_by_ip(publicip)

        user = {
            # Required
            "username": data["username"],
            "email": data["email"],
            "password": generate_password_hash(data["password"]),
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "age": age,
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
            "location": location,
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
        send_verification_email(data["email"], token, user['first_name'])
        
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
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
            
        # Find user and check credentials
        user = UserModel.find_by_email(data['email'])
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
    

@user_bp.route('/forgot_password', methods=['POST'])
def forgot_password():
   try:
       data = request.get_json()
       email = data.get('email')
       
       if not email:
           return jsonify({'error': 'Email is required'}), 400
           
       user = UserModel.find_by_email(email)
       print("User: ", user)
       if not user:
           # for security reasons, we don't want to reveal if the email is registered
           return jsonify({
               'message': 'If your email is registered, you will receive a password reset link'
           }), 200
           
       # Generate temporary token
       reset_token = jwt.encode(
           {
               'user_id': str(user['_id']),
               'exp': datetime.utcnow() + timedelta(hours=1)  # token expires in 1 hour
           },
           current_app.config['SECRET_KEY'],
           algorithm='HS256'
       )
       
       # send reset password email
       send_reset_password_email(email, reset_token)
       
       return jsonify({
           'message': 'If your email is registered, you will receive a password reset link'
       }), 200
       
   except Exception as e:
       return jsonify({'error': str(e)}), 500


@user_bp.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
   try:
       data = request.get_json()
       new_password = data.get('password')

       if not new_password:
           return jsonify({'error': 'New password is required'}), 400
       
       # Validate new password
       is_valid, error_msg = validate_password(new_password)
       if not is_valid:
            return jsonify({'error': error_msg}), 400
          
       # Verify token
       try:
           payload = jwt.decode(
               token,
               current_app.config['SECRET_KEY'],
               algorithms=['HS256']
           )
       except jwt.ExpiredSignatureError:
           return jsonify({'error': 'Reset link has expired'}), 400
       except jwt.InvalidTokenError:
           return jsonify({'error': 'Invalid reset link'}), 400
           
       # update password
       user_id = payload['user_id']
       hashed_password = generate_password_hash(new_password)
       
       UserModel.update_password(user_id, hashed_password)
       
       return jsonify({'message': 'Password updated successfully'}), 200
       
   except Exception as e:
       return jsonify({'error': str(e)}), 500


@user_bp.route('/my_user_info', methods=['GET'])
@jwt_required()
def my_user_info():
   try:
       current_user_id = get_jwt_identity()
       user = UserModel.find_by_id(current_user_id)
       
       if not user:
           return jsonify({'error': 'User not found'}), 404
           
       # find profile photo
       profile_photo = next(
           (photo for photo in user.get('photos', []) if photo.get('is_profile')),
           None  # default value if not found
       )

       user_info = {
           'username': user.get('username'),
           'first_name': user.get('first_name'),
           'last_name': user.get('last_name'),
           'email': user.get('email'),
           'profile_photo': profile_photo.get('url') if profile_photo else None
       }
       
       return jsonify(user_info), 200
       
   except Exception as e:
       return jsonify({'error': str(e)}), 500


@user_bp.route('/update_user', methods=['PUT'])
@jwt_required()
def update_user():
   try:
       current_user_id = get_jwt_identity()
       data = request.get_json()
       
       # verify user
       user = UserModel.find_by_id(current_user_id)
       if not user:
           return jsonify({'error': 'User not found'}), 404

       # validate fields
       if 'username' in data:
           # verify length
           if len(data['username']) > 12:
               return jsonify({'error': 'Username must be 12 characters or less'}), 400
           # veryfy username is not in use
           existing = UserModel.find_by_username(data['username'])
           if existing and str(existing['_id']) != current_user_id:
               return jsonify({'error': 'Username already exists'}), 400

       if 'email' in data:
           # Verify email is not in use
           existing = UserModel.find_by_email(data['email'])
           if existing and str(existing['_id']) != current_user_id:
               return jsonify({'error': 'Email already exists'}), 400

       if 'password' in data:
           # validate password
           is_valid, error_msg = validate_password(data['password'])
           if not is_valid:
               return jsonify({'error': error_msg}), 400
           # Hash password
           data['password'] = generate_password_hash(data['password'])

       # allowed fields to update
       allowed_fields = ['username', 'first_name', 'last_name', 'email', 'password']
       update_data = {k: v for k, v in data.items() if k in allowed_fields}

       if not update_data:
           return jsonify({'error': 'No valid fields to update'}), 400

       # update user
       result = UserModel.update_profile(current_user_id, update_data)
       
       return jsonify({
           'message': 'User updated successfully',
           'updated_fields': list(update_data.keys())
       }), 200
       
   except Exception as e:
       return jsonify({'error': str(e)}), 500