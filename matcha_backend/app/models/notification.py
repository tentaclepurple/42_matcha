# app/models/notification.py


from ..config.database import mongo
from bson import ObjectId
from datetime import datetime

class NotificationModel:
    @staticmethod
    def create(user_id: str, type: str, from_user_id: str = None) -> bool:
        """
        Create a new notification
        Args:
            user_id: User who receives the notification
            type: Type of notification (profile_view, like, rmlike, unlike, match, message)
            from_user_id: User who triggered the notification
        """
        try:
            notification = {
                "user_id": ObjectId(user_id),
                "type": type,
                "from_user_id": ObjectId(from_user_id) if from_user_id else None,
                "created_at": datetime.utcnow(),
                "read": False
            }

            result = mongo.db.notifications.insert_one(notification)
            return bool(result.inserted_id)
            
        except Exception as e:
            print(f"Error creating notification: {str(e)}")
            return False

    @staticmethod
    def get_unread(user_id: str):
        """Get unread notifications for a user"""
        try:
            pipeline = [
                {
                    "$match": {
                        "user_id": ObjectId(user_id),
                        "read": False
                    }
                },
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "from_user_id",
                        "foreignField": "_id",
                        "as": "from_user"
                    }
                },
                {
                    "$addFields": {
                        "from_user": {
                            "$cond": {
                                "if": {"$eq": [{"$size": "$from_user"}, 0]},
                                "then": None,
                                "else": {"$arrayElemAt": ["$from_user", 0]}
                            }
                        }
                    }
                },
                {
                    "$project": {
                        "_id": {"$toString": "$_id"},
                        "type": 1,
                        "created_at": 1,
                        "read": 1,
                        "from_user": {
                            "$cond": {
                                "if": {"$eq": ["$from_user", None]},
                                "then": None,
                                "else": {
                                    "_id": {"$toString": "$from_user._id"},
                                    "username": "$from_user.username"
                                }
                            }
                        }
                    }
                },
                {
                    "$sort": {"created_at": -1}
                }
            ]
                
            return list(mongo.db.notifications.aggregate(pipeline))
            
        except Exception as e:
            print(f"Error getting notifications: {str(e)}")
            return []

    @staticmethod
    def mark_as_read(user_id: str, notification_ids: list = None):
        """
        Mark notifications as read
        Args:
            user_id: User whose notifications to mark
            notification_ids: Optional list of specific notification IDs to mark
        """
        try:
            query = {"user_id": ObjectId(user_id)}
            if notification_ids:
                query["_id"] = {"$in": [ObjectId(id) for id in notification_ids]}
            
            result = mongo.db.notifications.update_many(
                query,
                {"$set": {"read": True}}
            )
            
            return result.modified_count
            
        except Exception as e:
            print(f"Error marking notifications as read: {str(e)}")
            return 0
    
    