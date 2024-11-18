# app/models/like.py


from ..config.database import mongo
from bson import ObjectId
from datetime import datetime


class LikeModel:
    @staticmethod
    def add_like(from_user_id: str, to_user_id: str, like_type: str):
        """Add a like or unlike"""
        if like_type not in ["like", "unlike"]:
            raise ValueError("Like type must be 'like' or 'unlike'")

        like = {
            "from_user_id": ObjectId(from_user_id),
            "to_user_id": ObjectId(to_user_id),
            "created_at": datetime.utcnow(),
            "type": like_type
        }
        
        return mongo.db.likes.insert_one(like)

    @staticmethod
    def check_is_match(user1_id: str, user2_id: str):
        """Check if two users have mutual likes"""
        matches = mongo.db.likes.count_documents({
            "$and": [
                {
                    "from_user_id": {"$in": [ObjectId(user1_id), ObjectId(user2_id)]},
                    "to_user_id": {"$in": [ObjectId(user1_id), ObjectId(user2_id)]},
                    "type": "like"
                }
            ]
        })
        return matches == 2

    @staticmethod
    def get_likes_received(user_id: str, like_type: str = None):
        """Get likes or unlikes received by a user"""
        match_query = {"to_user_id": ObjectId(user_id)}
        if like_type:
            match_query["type"] = like_type

        pipeline = [
            {
                "$match": match_query
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
                "$unwind": "$from_user"
            },
            {
                "$project": {
                    "type": 1,
                    "created_at": 1,
                    "from_user": {
                        "_id": 1,
                        "username": 1,
                        "first_name": 1,
                        "last_name": 1
                    }
                }
            },
            {
                "$sort": {"created_at": -1}
            }
        ]
        
        return list(mongo.db.likes.aggregate(pipeline))
    
    @staticmethod
    def check_like_status(from_user_id: str, to_user_id: str) -> dict:
        """
        Check all like/unlike interactions between users
        Returns: dict with like and unlike status
        """
        like_exists = mongo.db.likes.find_one({
            "from_user_id": ObjectId(from_user_id),
            "to_user_id": ObjectId(to_user_id),
            "type": "like"
        })
        
        unlike_exists = mongo.db.likes.find_one({
            "from_user_id": ObjectId(from_user_id),
            "to_user_id": ObjectId(to_user_id),
            "type": "unlike"
        })
        
        return {
            "has_like": bool(like_exists),
            "has_unlike": bool(unlike_exists)
        }

    @staticmethod
    def get_mutual_status(user1_id: str, user2_id: str) -> dict:
        """
        Get complete like/unlike status between two users
        """
        outgoing = LikeModel.check_like_status(user1_id, user2_id)
        incoming = LikeModel.check_like_status(user2_id, user1_id)
        
        return {
            "liked_by_me": outgoing["has_like"],
            "likes_me": outgoing["has_unlike"],
            "unliked_by_me": incoming["has_like"],
            "unlikes_me": incoming["has_unlike"],
            "is_match": outgoing["has_like"] and incoming["has_like"]
        }
