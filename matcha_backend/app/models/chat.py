# app/models/chat.py

from ..config.database import mongo
from bson import ObjectId
from datetime import datetime
from typing import Optional, Dict, Any, List
from .notification import NotificationModel


class ChatModel:
    @staticmethod
    def send_message(from_user_id: str, to_user_id: str, content: str, msg_type: str = "text") -> bool:
        """
        Send a new message
        Args:
            from_user_id: Sender's user ID
            to_user_id: Recipient's user ID
            content: Message content or image URL
            msg_type: Message type (text/image)
        Returns:
            bool: True if message was sent successfully
        """
        try:
            message = {
                "from_user_id": ObjectId(from_user_id),
                "to_user_id": ObjectId(to_user_id),
                "content": content,
                "type": msg_type,
                "created_at": datetime.utcnow(),
                "read": False
            }
            
            result = mongo.db.chat_messages.insert_one(message)
            
			# Create notification
            NotificationModel.create(
				user_id=to_user_id,
				type="message",
				from_user_id=from_user_id
			)

            return bool(result.inserted_id)
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return False

    @staticmethod
    def get_conversation_messages(user1_id: str, user2_id: str, limit: int = 50, after_date: datetime = None) -> List[Dict]:
        """
        Get messages between two users
        Args:
            user1_id: First user's ID
            user2_id: Second user's ID
            limit: Maximum number of messages to return
            after_date: Get messages after this date (for polling)
        Returns:
            List of messages
        """
        try:
            query = {
                "$or": [
                    {
                        "from_user_id": ObjectId(user1_id),
                        "to_user_id": ObjectId(user2_id)
                    },
                    {
                        "from_user_id": ObjectId(user2_id),
                        "to_user_id": ObjectId(user1_id)
                    }
                ]
            }
            
            if after_date:
                query["created_at"] = {"$gt": after_date}

            return list(
                mongo.db.chat_messages.find(query)
                .sort("created_at", -1)
                .limit(limit)
            )
            
        except Exception as e:
            print(f"Error getting messages: {str(e)}")
            return []

    @staticmethod
    def get_conversations(user_id: str) -> List[Dict]:
        """
        Get all conversations for a user (users they have exchanged messages with)
        Args:
            user_id: User ID
        Returns:
            List of conversations with last message and unread count
        """
        try:
            pipeline = [
                # Match messages where user is sender or receiver
                {
                    "$match": {
                        "$or": [
                            {"from_user_id": ObjectId(user_id)},
                            {"to_user_id": ObjectId(user_id)}
                        ]
                    }
                },
                # Group by the other user in the conversation
                {
                    "$group": {
                        "_id": {
                            "$cond": [
                                {"$eq": ["$from_user_id", ObjectId(user_id)]},
                                "$to_user_id",
                                "$from_user_id"
                            ]
                        },
                        "last_message": {"$first": "$$ROOT"},
                        "unread_count": {
                            "$sum": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {"$eq": ["$to_user_id", ObjectId(user_id)]},
                                            {"$eq": ["$read", False]}
                                        ]
                                    },
                                    1,
                                    0
                                ]
                            }
                        }
                    }
                },
                # Lookup other user's info
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "other_user"
                    }
                },
                {"$unwind": "$other_user"},
                # Project needed fields
                {
                    "$project": {
                        "other_user": {
                            "_id": 1,
                            "username": 1,
                            "online": 1,
                            "last_connection": 1,
                            "photos": {
                                "$filter": {
                                    "input": "$other_user.photos",
                                    "as": "photo",
                                    "cond": {"$eq": ["$$photo.is_profile", True]}
                                }
                            }
                        },
                        "last_message": 1,
                        "unread_count": 1
                    }
                },
                {"$sort": {"last_message.created_at": -1}}
            ]
            
            return list(mongo.db.chat_messages.aggregate(pipeline))
            
        except Exception as e:
            print(f"Error getting conversations: {str(e)}")
            return []

    @staticmethod
    def mark_messages_as_read(from_user_id: str, to_user_id: str) -> int:
        """
        Mark all messages from a user to another as read
        Returns number of messages marked as read
        """
        try:
            result = mongo.db.chat_messages.update_many(
                {
                    "from_user_id": ObjectId(from_user_id),
                    "to_user_id": ObjectId(to_user_id),
                    "read": False
                },
                {"$set": {"read": True}}
            )
            return result.modified_count
            
        except Exception as e:
            print(f"Error marking messages as read: {str(e)}")
            return 0