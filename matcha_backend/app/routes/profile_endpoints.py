# app/routes/profile_endpoints.py

import os
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

from werkzeug.utils import secure_filename
from ..models.user import UserModel
from ..models.profile_view import ProfileViewModel
from ..models.like import LikeModel
from ..models.notification import NotificationModel


UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


profile_bp = Blueprint('profiles', __name__)


@profile_bp.route('/update_profile', methods=['POST'])
@jwt_required()
def update_profile():
   try:
       current_user_id = get_jwt_identity()
       data = request.get_json()

       required_fields = ['gender', 'sexual_preferences', 'biography', 'interests']
       for field in required_fields:
           if field not in data:
               return jsonify({'error': f'Mandatory field: {field}'}), 400

       if data['gender'] not in ['male', 'female', 'other']:
           return jsonify({'error': 'Gender selection not allowed at the moment'}), 400

       if data['sexual_preferences'] not in ['male', 'female', 'bisexual']:
           return jsonify({'error': 'Sexual preference not allowed at the moment'}), 400

       if 'location' in data:
           if not isinstance(data['location'], dict) or \
              'type' not in data['location'] or \
              'coordinates' not in data['location'] or \
              data['location']['type'] != 'Point' or \
              not isinstance(data['location']['coordinates'], list) or \
              len(data['location']['coordinates']) != 2:
               return jsonify({'error': 'Invalid location format'}), 400

       # Manage interests
       interests = data.pop('interests')
       if not all(isinstance(tag, str) for tag in interests):
           return jsonify({'error': 'Invalid tag format'}), 400
       
       # update interests
       UserModel.update_interests(current_user_id, interests)

       # update profile
       result = UserModel.update_profile(current_user_id, data)

       return jsonify({
           'message': 'Profile updated successfully',
           'profile_completed': True
       }), 200

   except Exception as e:
       return jsonify({'error': str(e)}), 500


@profile_bp.route('/update_avatar/<int:index>', methods=['PUT'])
@jwt_required()
def set_profile_photo(index):
    if not 0 <= index <= 4:
        return jsonify({'error': 'Invalid index'}), 400
        
    try:
        current_user_id = get_jwt_identity()
        result = UserModel.set_profile_photo(current_user_id, index)
        
        return jsonify({'message': 'Profile photo updated'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/my_profile_info', methods=['GET'])
@jwt_required()
def my_profile_info():
   try:
       current_user_id = get_jwt_identity()
       user = UserModel.find_by_id(current_user_id)
       
       if not user:
           return jsonify({'error': 'User not found'}), 404
           
       profile_info = {
           # Profile
           'username': user.get('username'),
           'gender': user.get('gender'),
           'sexual_preferences': user.get('sexual_preferences'),
           'biography': user.get('biography'),
           'interests': user.get('interests', []),
           'photos': user.get('photos', []),
           'location': user.get('location'),
           'fame_rating': user.get('fame_rating'),
           
           # Other
           'blocked_users': user.get('blocked_users', []),
           'reported': user.get('reported', False),
           
           # Status
           'online': user.get('online'),
           'last_connection': user.get('last_connection'),
           'profile_completed': user.get('profile_completed'),
       }
       
       return jsonify(profile_info), 200
       
   except Exception as e:
       return jsonify({'error': str(e)}), 500


@profile_bp.route('/profile_info/<user_identifier>', methods=['GET'])
@jwt_required()
def get_user_profile(user_identifier):
    """
    Obtiene el perfil público de un usuario por su ID o username
    
    Args:
        user_identifier: Puede ser el ObjectId o el username del usuario
    """
    try:
        current_user_id = get_jwt_identity()
        
        # first try to find by ID (for ObjectId)
        user = None
        try:
            if len(user_identifier) == 24:  # id length
                user = UserModel.find_by_id(user_identifier)
        except:
            pass
            
        # if not found, try to find by username
        if not user:
            user = UserModel.find_by_username(user_identifier)
            
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Verify if user is blocked
        if ObjectId(current_user_id) in user.get('blocked_users', []):
            return jsonify({'error': 'Profile not available'}), 403

        user_id = str(user['_id'])
        is_own_profile = user_id == current_user_id

        ProfileViewModel.record_view(
            viewer_id=current_user_id,
            viewed_id=str(user['_id'])
        )
        
        NotificationModel.create(
            user_id=user_id,
            type="profile_view",
            from_user_id=current_user_id
        )
        
        like_status = LikeModel.get_mutual_status(current_user_id, user_id)

        profile_info = {
            'user_id': str(user['_id']),
            'username': user['username'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'age': user.get('age'),
            'gender': user.get('gender'),
            'sexual_preferences': user.get('sexual_preferences'),
            'biography': user.get('biography'),
            'interests': user.get('interests', []),
            'photos': user.get('photos', []),
            'location': user.get('location'),
            'fame_rating': user.get('fame_rating'),
            'online': user.get('online'),
            'last_connection': user.get('last_connection'),
            'profile_completed': user.get('profile_completed', False),
            'blocked_users': user.get('blocked_users', []),
            'reported': user.get('reported', False),
            'verified': user.get('verified', False),
            'created_at': user.get('created_at'),
            'like_info': like_status if not is_own_profile else None,
            
            'is_own_profile': str(user['_id']) == current_user_id
        }
        
        return jsonify(profile_info), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
