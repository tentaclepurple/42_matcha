# app/routes/interaction_endpoints.py


from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import UserModel


interaction_bp = Blueprint('interaction', __name__)


@interaction_bp.route('/report/<user_id>', methods=['POST'])
@jwt_required()
def report_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user exists
        user = UserModel.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Check if trying to report self
        if user_id == current_user_id:
            return jsonify({'error': 'Cannot report yourself'}), 400
            
        # Report user
        result = UserModel.report_user(user_id)
        
        return jsonify({
            'message': 'User reported successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
