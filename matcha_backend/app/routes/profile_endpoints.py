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


@profile_bp.route('/create_profile', methods=['POST'])
@jwt_required()
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        required_fields = ['gender', 'sexual_preferences', 'biography', 'interests']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Mandatory field: {field}'}), 400

        if 'gender' in data and data['gender'] not in ['male', 'female', 'other']:
            return jsonify({'error': 'Gender selection not allowed at the moment'}), 400

        if 'sexual_preferences' in data:
            valid_preferences = ['male', 'female', 'bisexual']
            if data["sexual_preferences"] not in valid_preferences:
                return jsonify({'error': 'Sexual preference not allowed at the moment'}), 400

        if 'location' in data:
            if not isinstance(data['location'], dict) or \
               'type' not in data['location'] or \
               'coordinates' not in data['location'] or \
               data['location']['type'] != 'Point' or \
               not isinstance(data['location']['coordinates'], list) or \
               len(data['location']['coordinates']) != 2:
                return jsonify({'error': 'Invalid location format'}), 400
        
        if 'interests' in data:
            # Opcional: validar formato de tags
            if not all(isinstance(tag, str) for tag in data['interests']):
                return jsonify({'error': 'Invalid tag format'}), 400
            
            # Actualizar intereses (esto actualizará ambas colecciones)
            UserModel.update_interests(current_user_id, data['interests'])

        result = UserModel.update_profile(current_user_id, data)

        return jsonify({
            'message': 'Profile updated successfully',
            'profile_completed': True
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/update_photo/<int:index>', methods=['PUT'])
@jwt_required()
def update_photo(index):
    if not 0 <= index <= 4:
        return jsonify({'error': 'Invalid index'}), 400
        
    try:
        current_user_id = get_jwt_identity()
        
        print("photo index\n", index)
        print("files\n", request.files)
        if 'photo' not in request.files:
            return jsonify({'error': 'No photo provided'}), 400
            
        photo = request.files['photo']
        
        # Validar archivo
        if not photo or not allowed_file(photo.filename):
            return jsonify({'error': 'Invalid file type'}), 400
            
        # Validar tamaño
        if request.content_length > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large. Maximum size is 5MB'}), 400
            
        # Obtener usuario y su foto actual
        user = UserModel.find_by_id(current_user_id)
        current_photo = user['photos'][index]['url']
        
        # Si la foto actual no es la default, borrarla
        if 'default' not in current_photo:
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, current_photo))
            except:
                pass  # Si falla el borrado, continuamos igual
        
        # Guardar nueva foto
        filename = secure_filename(f"{current_user_id}_{index}_{photo.filename}")
        path = os.path.join(UPLOAD_FOLDER, filename)
        photo.save(path)
        
        # Actualizar en base de datos
        photo_data = {
            'url': path,
            'is_profile': user['photos'][index]['is_profile'],
            'uploaded_at': datetime.utcnow()
        }
        
        UserModel.update_photo(current_user_id, index, photo_data)
        
        return jsonify({
            'message': 'Photo updated successfully',
            'photo': photo_data
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
