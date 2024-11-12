# app/models/profile_view.py


class ProfileViewModel:
    @staticmethod
    def record_view(viewer_id: str, viewed_id: str):
        """Record a profile view"""
        view = {
            "viewer_id": ObjectId(viewer_id),
            "viewed_id": ObjectId(viewed_id),
            "viewed_at": datetime.utcnow()
        }
        
        return mongo.db.profile_views.insert_one(view)

    @staticmethod
    def get_profile_viewers(user_id: str, limit: int = 10):
        """Get list of users who viewed a profile"""
        pipeline = [
            {
                "$match": {
                    "viewed_id": ObjectId(user_id)
                }
            },
            {
                # Agrupar por viewer_id para evitar duplicados
                "$group": {
                    "_id": "$viewer_id",
                    "last_view": {"$max": "$viewed_at"},
                    "view_count": {"$sum": 1}
                }
            },
            {
                # Obtener información del viewer
                "$lookup": {
                    "from": "users",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "viewer"
                }
            },
            {
                "$unwind": "$viewer"
            },
            {
                "$project": {
                    "viewer": {
                        "_id": 1,
                        "username": 1,
                        "first_name": 1,
                        "last_name": 1
                    },
                    "last_view": 1,
                    "view_count": 1
                }
            },
            {
                "$sort": {"last_view": -1}
            },
            {
                "$limit": limit
            }
        ]
        
        return list(mongo.db.profile_views.aggregate(pipeline))

    @staticmethod
    def get_view_stats(user_id: str):
        """Get profile view statistics"""
        pipeline = [
            {
                "$match": {
                    "viewed_id": ObjectId(user_id)
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_views": {"$sum": 1},
                    "unique_viewers": {"$addToSet": "$viewer_id"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "total_views": 1,
                    "unique_viewers": {"$size": "$unique_viewers"}
                }
            }
        ]
        
        stats = list(mongo.db.profile_views.aggregate(pipeline))
        return stats[0] if stats else {"total_views": 0, "unique_viewers": 0}
