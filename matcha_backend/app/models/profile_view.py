from ..config.database import mongo
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class ProfileViewModel:
    @staticmethod
    def record_view(viewer_id: str, viewed_id: str):
        """
        Record a profile view, preventing duplicates within a timeframe
        
        Args:
            viewer_id: ID of the user viewing the profile
            viewed_id: ID of the user whose profile is being viewed
            
        Returns:
            The result of the insert operation or None if it's a duplicate within timeframe
        """
        # Convert string IDs to ObjectId
        viewer_oid = ObjectId(viewer_id)
        viewed_oid = ObjectId(viewed_id)
        
        # Define the timeframe for considering a view as duplicate (e.g., 24 hours)
        duplicate_window = datetime.utcnow() - timedelta(hours=24)
        
        # Check for existing view within the timeframe
        existing_view = mongo.db.profile_views.find_one({
            "viewer_id": viewer_oid,
            "viewed_id": viewed_oid,
            "viewed_at": {"$gte": duplicate_window}
        })
        
        # If no recent view exists, record the new view
        if not existing_view:
            view = {
                "viewer_id": viewer_oid,
                "viewed_id": viewed_oid,
                "viewed_at": datetime.utcnow()
            }
            return mongo.db.profile_views.insert_one(view)
            
        return None

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
                # Group by viewer_id to avoid duplicates
                "$group": {
                    "_id": "$viewer_id",
                    "last_view": {"$max": "$viewed_at"},
                    "view_count": {"$sum": 1}
                }
            },
            {
                # Get viewer information
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
