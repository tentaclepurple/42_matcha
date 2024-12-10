# app/routes/notification_endpoints.py

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.notification import NotificationModel


notification_bp = Blueprint('notifications', __name__)


@notification_bp.route('/unread', methods=['GET'])
@jwt_required()
def get_unread_notifications():
    """Get all unread notifications for the current user"""
    try:
        current_user_id = get_jwt_identity()
        print("current_user_id", current_user_id)
        notifications = NotificationModel.get_unread(current_user_id)
        
        return jsonify({
            'notifications': notifications,
            'count': len(notifications)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notification_bp.route('/mark_as_read', methods=['POST'])
@jwt_required()
def mark_notifications_read():
    """Mark all notifications as read for the current user"""
    try:
        current_user_id = get_jwt_identity()
        count = NotificationModel.mark_as_read(current_user_id)
        
        return jsonify({
            'message': f'Marked {count} notifications as read'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notification_bp.route('/mark_as_read/<notification_id>', methods=['POST'])
@jwt_required()
def mark_notifications_read(notification_id):
    """Mark all notifications as read for the current user"""
    try:
        current_user_id = get_jwt_identity()
        count = NotificationModel.mark_as_read(current_user_id, [notification_id])
        
        return jsonify({
            'message': f'Marked {count} notifications as read'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
