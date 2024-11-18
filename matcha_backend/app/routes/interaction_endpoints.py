# app/routes/interaction_endpoints.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from ..models.user import UserModel


interaction_bp = Blueprint('interaction', __name__)


def get_user_by_identifier(identifier: str):
    """
    Find user by ID or username
    
    Args:
        identifier: User ID or username
        
    Returns:
        dict: User found or None
    """
    try:
        if len(identifier) == 24:
            user = UserModel.find_by_id(identifier)
            if user:
                return user
    except:
        pass
    
    return UserModel.find_by_username(identifier)


@interaction_bp.route('/report/<user_identifier>', methods=['POST'])
@jwt_required()
def report_user(user_identifier):
    try:
        current_user_id = get_jwt_identity()
        
        # Find user by ID or username
        user = get_user_by_identifier(user_identifier)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        user_id = str(user['_id'])
            
        # Check if trying to report self
        if user_id == current_user_id:
            return jsonify({'error': 'Cannot report yourself'}), 400
            
        # Report user
        result = UserModel.report_user(user_id)
        
        return jsonify({
            'message': f'User {user["username"]} reported successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@interaction_bp.route('/block/<user_identifier>', methods=['POST'])
@jwt_required()
def block_user(user_identifier):
    try:
        current_user_id = get_jwt_identity()
        
        # Find user to block
        user_to_block = get_user_by_identifier(user_identifier)
        if not user_to_block:
            return jsonify({'error': 'User to block not found'}), 404
            
        user_to_block_id = str(user_to_block['_id'])
            
        # Check if trying to block self
        if user_to_block_id == current_user_id:
            return jsonify({'error': 'Cannot block yourself'}), 400
        
        # Block user
        result = UserModel.block_user(current_user_id, user_to_block_id)
        
        return jsonify({
            'message': f'User {user_to_block["username"]} blocked successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@interaction_bp.route('/unblock/<user_identifier>', methods=['POST'])
@jwt_required()
def unblock_user(user_identifier):
    try:
        current_user_id = get_jwt_identity()
        
        # Find user to unblock
        user_to_unblock = get_user_by_identifier(user_identifier)
        if not user_to_unblock:
            return jsonify({'error': 'User to unblock not found'}), 404
            
        user_to_unblock_id = str(user_to_unblock['_id'])
        
        # Unblock user
        result = UserModel.unblock_user(current_user_id, user_to_unblock_id)
        
        return jsonify({
            'message': f'User {user_to_unblock["username"]} unblocked successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
