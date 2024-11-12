# app/models/like.py

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
