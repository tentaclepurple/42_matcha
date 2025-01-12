# app/routes/chat_endpoints.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.chat import ChatModel
from ..models.user import UserModel
from ..models.like import LikeModel
from ..models.iamatcha import BotModel
from ..models.bot_profiles import BOT_PROFILES
from bson import ObjectId
from datetime import datetime


chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    """Get all conversations for the current user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get all conversations
        conversations = ChatModel.get_conversations(current_user_id)
        
        # Format response
        response = []
        for conv in conversations:
            # Get last message info
            last_message = conv['last_message']
            is_from_me = str(last_message['from_user_id']) == current_user_id
            
            # Get other user info
            other_user = conv['other_user']
            profile_photo = next(
                (photo['url'] for photo in other_user.get('photos', []) 
                if photo.get('is_profile')), 
                None
            )
            
            is_match = LikeModel.check_is_match(str(other_user['_id']), current_user_id)
            if is_match:
                response.append({
                    'user': {
                        'user_id': str(other_user['_id']),
                        'username': other_user['username'],
                        'profile_photo': profile_photo,
                        'online': other_user.get('online', False),
                        'last_connection': other_user.get('last_connection')
                    },
                    'last_message': {
                        'content': last_message['content'],
                        'type': last_message['type'],
                        'from_me': is_from_me,
                        'created_at': last_message['created_at'],
                        'read': last_message['read']
                    },
                    'unread_count': conv['unread_count']
                })
            
        return jsonify({
            'conversations': response
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/messages/<user_identifier>', methods=['GET'])
@jwt_required()
def get_messages(user_identifier):
    """Get messages between current user and specified user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Find other user
        other_user = None
        try:
            if len(user_identifier) == 24:
                other_user = UserModel.find_by_id(user_identifier)
        except:
            pass
            
        if not other_user:
            other_user = UserModel.find_by_username(user_identifier)
            
        if not other_user:
            return jsonify({'error': 'User not found'}), 404
            
        other_user_id = str(other_user['_id'])
        
        # Verify match exists
        is_match = LikeModel.check_is_match(current_user_id, other_user_id)
        if not is_match:
            return jsonify({'error': 'Cannot chat with this user - no match exists'}), 403
            
        # Get query parameters
        limit = request.args.get('limit', default=50, type=int)
        after = request.args.get('after', type=str)
        
        # Convert 'after' to datetime if provided
        after_date = None
        if after:
            try:
                after_date = datetime.fromisoformat(after.replace('Z', '+00:00'))
            except:
                return jsonify({'error': 'Invalid timestamp format'}), 400
        
        # Get messages
        messages = ChatModel.get_conversation_messages(
            current_user_id,
            other_user_id,
            limit=limit,
            after_date=after_date
        )
        
        # Mark received messages as read
        ChatModel.mark_messages_as_read(other_user_id, current_user_id)
        
        profile_photo = next(
                (photo['url'] for photo in other_user.get('photos', []) 
                if photo.get('is_profile')), 
                None
            )

        # Format response
        response = [{
            'message_id': str(msg['_id']),
            'content': msg['content'],
            'type': msg['type'],
            'from_me': str(msg['from_user_id']) == current_user_id,
            'created_at': msg['created_at'],
            'read': msg['read']
        } for msg in messages]
        
        return jsonify({
            'other_user': {
                'user_id': other_user_id,
                'username': other_user['username'],
                'profile_photo': profile_photo,
                'online': other_user.get('online', False),
                'last_connection': other_user.get('last_connection')
            },
            'messages': response
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/send/<user_identifier>', methods=['POST'])
@jwt_required()
def send_message(user_identifier):
    """Send a message to a user"""
    try:
        current_user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'Current user not found'}), 404

        # Validate request
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({'error': 'Message content is required'}), 400
            
        content = data['content'].strip()
        if not content:
            return jsonify({'error': 'Message cannot be empty'}), 400
            
        msg_type = data.get('type', 'text')
        if msg_type not in ['text', 'image']:
            return jsonify({'error': 'Invalid message type'}), 400
            
        # Find recipient
        recipient = None
        try:
            if len(user_identifier) == 24:
                recipient = UserModel.find_by_id(user_identifier)
        except:
            pass
            
        if not recipient:
            recipient = UserModel.find_by_username(user_identifier)
            
        if not recipient:
            return jsonify({'error': 'Recipient not found'}), 404

        # Verify match exists
        recipient_id = str(recipient['_id'])

        # Check if recipient has blocked current user
        if ObjectId(current_user_id) in recipient.get('blocked_users', []):
            return jsonify({'error': 'Cannot send message to this user'}), 403

        # Check if current user has blocked recipient
        if ObjectId(recipient_id) in current_user.get('blocked_users', []):
            return jsonify({'error': 'Cannot send message to a user you have blocked'}), 403

        is_match = LikeModel.check_is_match(current_user_id, recipient_id)

        if not is_match:
            return jsonify({'error': 'Cannot send message - no match exists'}), 403

        # Check if recipient is a bot
        bot = next((bot for bot in BOT_PROFILES.values() 
                    if bot["username"] == recipient["username"] or 
                    str(bot["_id"]) == str(recipient["_id"])), None)
        
        if bot:
            ChatModel.send_message(
                from_user_id=current_user_id,
                to_user_id=str(bot["_id"]),
                content=content,
                msg_type='text'
            )
            
            # Process bot response
            if BotModel.handle_user_message(current_user_id, content, str(bot["_id"])):
                return jsonify({'message': 'Message sent and processed'}), 200
            else:
                return jsonify({'error': 'Failed to process message'}), 401
            
        
            
        # Send message
        success = ChatModel.send_message(
            from_user_id=current_user_id,
            to_user_id=recipient_id,
            content=content,
            msg_type=msg_type
        )
        
        if not success:
            return jsonify({'error': 'Failed to send message'}), 500
            
        return jsonify({'message': 'Message sent successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/read/<user_identifier>', methods=['PUT'])
@jwt_required()
def mark_read(user_identifier):
    """Mark all messages from a user as read"""
    try:
        current_user_id = get_jwt_identity()
        
        # Find sender
        sender = None
        try:
            if len(user_identifier) == 24:
                sender = UserModel.find_by_id(user_identifier)
        except:
            pass
            
        if not sender:
            sender = UserModel.find_by_username(user_identifier)
            
        if not sender:
            return jsonify({'error': 'User not found'}), 404
            
        # Mark messages as read
        count = ChatModel.mark_messages_as_read(
            from_user_id=str(sender['_id']),
            to_user_id=current_user_id
        )
        
        return jsonify({
            'message': f'Marked {count} messages as read'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
