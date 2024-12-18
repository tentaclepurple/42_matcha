# app/routes/interaction_endpoints.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from ..config.database import mongo
from ..models.user import UserModel
from ..models.like import LikeModel
from ..models.notification import NotificationModel
from ..models.iamatcha import BotModel
from ..models.bot_profiles import BOT_PROFILES


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


@interaction_bp.route('/like/<user_identifier>', methods=['POST'])
@jwt_required()
def toggle_like(user_identifier):
    try:
        current_user_id = get_jwt_identity()
        user = get_user_by_identifier(user_identifier)
        this_user = UserModel.find_by_id(current_user_id)
        profile_photos = [photo for photo in this_user['photos'] 
                         if photo['is_profile'] and photo['url'] != 'static/default/default.svg']

        if not profile_photos:
            return jsonify({'error': 'You must set a valid profile photo before liking other users'}), 400

        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if current_user_id in [str(blocked_id) for blocked_id in user.get('blocked_users', [])]:
            return jsonify({'error': 'This user had blocked you'}), 400
            
        to_user_id = str(user['_id'])
        # Check if trying to like self
        if to_user_id == current_user_id:
            return jsonify({'error': 'Cannot like yourself'}), 400

        # Check if user is a bot
        bot = next((bot for bot in BOT_PROFILES.values() 
                    if bot["username"] == user["username"] or 
                    str(bot["_id"]) == to_user_id), None)

        # Check existing interactions
        existing_like = mongo.db.likes.find_one({
            "from_user_id": ObjectId(current_user_id),
            "to_user_id": ObjectId(to_user_id),
            "type": "like"
        })

        
        existing_unlike = mongo.db.likes.find_one({
            "from_user_id": ObjectId(current_user_id),
            "to_user_id": ObjectId(to_user_id),
            "type": "unlike"
        })
        
        if existing_like:
            # If like exists, remove it
            mongo.db.likes.delete_one({"_id": existing_like["_id"]})
            UserModel.update_fame_rating(to_user_id, -13)
            NotificationModel.create(
                user_id=to_user_id,
                type="rmlike",
                from_user_id=current_user_id
            )
            return jsonify({'message': 'Like removed', 'like_removed': True}), 200
            
        # Remove unlike if exists and add like
        if existing_unlike:
            mongo.db.likes.delete_one({"_id": existing_unlike["_id"]})
            UserModel.update_fame_rating(to_user_id, 7)
            
        # Add new like
        LikeModel.add_like(current_user_id, to_user_id, "like")
        UserModel.update_fame_rating(to_user_id, 13)

        # Create like notification
        NotificationModel.create(
            user_id=to_user_id,
            type="like",
            from_user_id=current_user_id
        )
        
        # Check if match occurs (if the other user had already liked us)
        other_user_like = mongo.db.likes.find_one({
            "from_user_id": ObjectId(to_user_id),
            "to_user_id": ObjectId(current_user_id),
            "type": "like"
        })

        if bot and not existing_like and other_user_like:
            # Inicia conversación con el bot específico
            BotModel.handle_user_like(current_user_id, to_user_id)
        
        is_match = bool(other_user_like)
        if is_match:
            # Create match notifications for both users
            NotificationModel.create(
                user_id=to_user_id,
                type="match",
                from_user_id=current_user_id
            )
            NotificationModel.create(
                user_id=current_user_id,
                type="match",
                from_user_id=to_user_id
            )
        
        return jsonify({
            'message': 'Like added',
            'is_match': is_match,
            'like_added': True
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@interaction_bp.route('/unlike/<user_identifier>', methods=['POST'])
@jwt_required()
def toggle_unlike(user_identifier):
    try:
        current_user_id = get_jwt_identity()
        user = get_user_by_identifier(user_identifier)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        if current_user_id in [str(blocked_id) for blocked_id in user.get('blocked_users', [])]:
            return jsonify({'error': 'This user had blocked you'}), 400

        to_user_id = str(user['_id'])

        # check if trying to unlike self
        if to_user_id == current_user_id:
            return jsonify({'error': 'Cannot unlike yourself'}), 400
        
        # Check existing interactions
        existing_unlike = mongo.db.likes.find_one({
            "from_user_id": ObjectId(current_user_id),
            "to_user_id": ObjectId(to_user_id),
            "type": "unlike"
        })
        
        existing_like = mongo.db.likes.find_one({
            "from_user_id": ObjectId(current_user_id),
            "to_user_id": ObjectId(to_user_id),
            "type": "like"
        })
        
        if existing_unlike:
            # If unlike exists, remove it
            mongo.db.likes.delete_one({"_id": existing_unlike["_id"]})
            UserModel.update_fame_rating(to_user_id, 7)
            return jsonify({'message': 'Unlike removed'}), 200
            
        # Remove like if exists and add unlike
        if existing_like:
            mongo.db.likes.delete_one({"_id": existing_like["_id"]})
            UserModel.update_fame_rating(to_user_id, -13)
            
        # Add new unlike
        LikeModel.add_like(current_user_id, to_user_id, "unlike")
        UserModel.update_fame_rating(to_user_id, -7)

        # Create unlike notification
        NotificationModel.create(
            user_id=to_user_id,
            type="unlike",
            from_user_id=current_user_id
        )
        
        return jsonify({'message': 'Unlike added'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
