from ..config.database import mongo
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from .iamatcha import BotModel


class UserModel:
    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> str:
        """
        Create a new user
        Returns: user_id
        Raises: ValueError if user already exists
        """
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

    @staticmethod
    def update_profile(user_id: str, profile_data: Dict[str, Any], is_location=False) -> bool:
        """
        Update user profile data
        Returns: True if successful
        """
        user = UserModel.find_by_id(user_id)
        print(f"---->PROFILE COMPLETED: {user['profile_completed']}")
        
        try:
            if not user['profile_completed'] and not is_location:
                # Select bot for user if not already selected
                if BotModel.handle_profile_completion(user_id):
                    pass
        except Exception as e:
            print(e)
            pass
        if not is_location:
            profile_data['profile_completed'] = True    

        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": profile_data}
        )
        
        return result.modified_count > 0

    @staticmethod
    def update_photo(user_id: str, index: int, photo_data: dict) -> bool:
        """Update specific photo by index"""
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {f"photos.{index}": photo_data}}
        )
        return result.modified_count > 0

    @staticmethod
    def set_profile_photo(user_id: str, index: int) -> bool:
        """Set photo as profile photo"""
        try:
            # first unmark all photos as profile
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"photos.$[].is_profile": False}}
            )
            
            # then mark selected photo as profile
            result = mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {f"photos.{index}.is_profile": True}}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            raise Exception(f"Error setting profile photo: {str(e)}")

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

    @staticmethod
    def update_interests(user_id: str, new_interests: list) -> bool:
        try:
            # get current interests
            user = mongo.db.users.find_one(
                {"_id": ObjectId(user_id)},
                {"interests": 1}
            )
            current_interests = user.get('interests', [])

            # decrement count of tags no longer in interests
            for tag in current_interests:
                if tag not in new_interests:
                    mongo.db.tags.update_one(
                        {"name": tag},
                        {"$inc": {"count": -1}}
                    )

            # increment	count of new interests
            for tag in new_interests:
                mongo.db.tags.update_one(
                    {"name": tag},
                    {"$inc": {"count": 1}},
                    upsert=True  # create if not exists
                )

            # update user interests
            result = mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"interests": new_interests}}
            )

            return result.modified_count > 0

        except Exception as e:
            raise Exception(f"Error updating interests: {str(e)}")

    @staticmethod
    def update_password(user_id: str, new_password: str) -> bool:
        """Update user password"""
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": new_password}}
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
    def unblock_user(user_id: str, blocked_user_id: str) -> bool:
        """Remove user from blocked list"""
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"blocked_users": ObjectId(blocked_user_id)}}
        )
        return result.modified_count > 0

    @staticmethod
    def increment_login_attempts(user_id: str) -> Dict[str, Any]:
        """
        Increment login attempts and lock account if necessary
        Returns: Updated user data
        """
        update_data = {
            "login_attempts": 1,
            "last_failed_login": datetime.utcnow()
        }
        
        # Get current attempts
        user = mongo.db.users.find_one(
            {"_id": ObjectId(user_id)},
            {"login_attempts": 1}
        )
        
        current_attempts = user.get('login_attempts', 0) + 1
        update_data['login_attempts'] = current_attempts
        
        # Lock account if max attempts reached
        if current_attempts >= 5:
            update_data['locked_until'] = datetime.utcnow() + timedelta(hours=24)
        
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def reset_login_attempts(user_id: str) -> bool:
        """Reset login attempts after successful login"""
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "login_attempts": 0,
                    "locked_until": None,
                    "last_failed_login": None,
                    "online": True,
                    "last_connection": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0

    @staticmethod
    def check_account_lock(user_id: str) -> Optional[datetime]:
        """
        Check if account is locked
        Returns: None if not locked, or datetime when lock expires
        """
        user = mongo.db.users.find_one(
            {"_id": ObjectId(user_id)},
            {"locked_until": 1}
        )
        
        if user and user.get('locked_until'):
            if datetime.utcnow() < user['locked_until']:
                return user['locked_until']
            else:
                # Reset if lock has expired
                UserModel.reset_login_attempts(user_id)
                return None
        return None
    
    @staticmethod
    def update_fame_rating(user_id: str, points: int) -> bool:
        """Update user's fame rating within bounds 0-100"""
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            [
                {
                    "$set": {
                        "fame_rating": {
                            "$min": [
                                100,
                                {"$max": [0, {"$add": ["$fame_rating", points]}]}
                            ]
                        }
                    }
                }
            ]
        )
        return result.modified_count > 0