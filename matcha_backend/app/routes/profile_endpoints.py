from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models.user import UserModel


profile_bp = Blueprint('profiles', __name__)


@profile_bp.route('/create_profile', methods=['POST'])
@jwt_required()
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        print("USER ID\n", current_user_id)
        print("DATA\n", data["sexual_preferences"])

        required_fields = ['gender', 'sexual_preferences', 'biography', 'interests']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Mandatory field: {field}'}), 400

        if 'gender' in data and data['gender'] not in ['male', 'female', 'other']:
            return jsonify({'error': 'Gender selection not allowed at the moment'}), 400

        if 'sexual_preferences' in data:
            valid_preferences = ['men', 'women', 'bisexual']
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

        result = UserModel.update_profile(current_user_id, data)

        return jsonify({
            'message': 'Profile updated successfully',
            'profile_completed': True
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
