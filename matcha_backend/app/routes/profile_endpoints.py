# app/routes/profile_endpoints.py

import os
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from ..models.user import UserModel


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
