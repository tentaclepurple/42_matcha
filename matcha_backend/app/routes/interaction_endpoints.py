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


@interaction_bp.route('/block', methods=['POST'])
@jwt_required()
def block_user():
   try:
       current_user_id = get_jwt_identity()
       data = request.get_json()
       
       # verify user_id is provided
       if not data.get('user_id'):
           return jsonify({'error': 'User ID to block is required'}), 400
           
       user_to_block = data['user_id']
       
       # Verify user exists
       blocked_user = UserModel.find_by_id(user_to_block)
       if not blocked_user:
           return jsonify({'error': 'User to block not found'}), 404
           
       # verify user is not trying to block themselves
       if user_to_block == current_user_id:
           return jsonify({'error': 'Cannot block yourself'}), 400
       
       # block user
       result = UserModel.block_user(current_user_id, user_to_block)
       
       return jsonify({
           'message': 'User blocked successfully'
       }), 200
       
   except Exception as e:
       return jsonify({'error': str(e)}), 500


@interaction_bp.route('/unblock', methods=['POST'])
@jwt_required()
def unblock_user():
   try:
       current_user_id = get_jwt_identity()
       data = request.get_json()
       
       if not data.get('user_id'):
           return jsonify({'error': 'User ID to unblock is required'}), 400
           
       user_to_unblock = data['user_id']
       
       result = UserModel.unblock_user(current_user_id, user_to_unblock)
       
       return jsonify({
           'message': 'User unblocked successfully'
       }), 200
       
   except Exception as e:
       return jsonify({'error': str(e)}), 500
