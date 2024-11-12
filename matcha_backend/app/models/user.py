from ..config.database import mongo
from bson import ObjectId
from datetime import datetime
from typing import Optional, Dict, Any


class UserModel:
    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> str:
        """
        Create a new user
        Returns: user_id
        Raises: ValueError if user already exists
        """
        # Verificar si existe
        existing_user = mongo.db.users.find_one({
            "$or": [
                {"username": user_data["username"]},
                {"email": user_data["email"]}
            ]
        })
        
        if existing_user:
            raise ValueError(f"User with username {user_data['username']} or email {user_data['email']} already exists")
            
        result = mongo.db.users.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def verify_user(user_id: str) -> bool:
        """
        Mark user as verified
        Returns: True if successful
        Raises: ValueError if user not found
        """
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"verified": True}}
        )
        if result.modified_count == 0:
            raise ValueError("User not found")
        return True

    @staticmethod
    def update_online_status(user_id: str, is_online: bool) -> bool:
        """Update online status and last connection time"""
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "online": is_online,
                    "last_connection": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0

    @staticmethod
    def update_profile(user_id: str, profile_data: Dict[str, Any]) -> bool:
        """
        Update user profile data
        Returns: True if successful
        """
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": profile_data}
        )
        return result.modified_count > 0

    @staticmethod
    def find_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Find user by ID"""
        try:
            return mongo.db.users.find_one({"_id": ObjectId(user_id)})
        except:
            return None

    @staticmethod
    def find_by_username(username: str) -> Optional[Dict[str, Any]]:
        """Find user by username"""
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def find_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Find user by email"""
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def report_user(user_id: str) -> bool:
        """Mark user as reported"""
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"reported": True}}
        )
        return result.modified_count > 0

    @staticmethod
    def block_user(user_id: str, blocked_user_id: str) -> bool:
        """Add user to blocked list"""
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"blocked_users": ObjectId(blocked_user_id)}}
        )
        return result.modified_count > 0

    @staticmethod
    def is_verified(user_id: str) -> bool:
        """Check if user is verified"""
        user = mongo.db.users.find_one(
            {"_id": ObjectId(user_id)},
            {"verified": 1}
        )
        return user and user.get("verified", False)