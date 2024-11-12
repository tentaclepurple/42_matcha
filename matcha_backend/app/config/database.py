from flask_pymongo import PyMongo
from schemas import *

mongo = PyMongo()


def init_db():
    """Create the database collections with validation and indexes."""
    try:
        # Create collections with validation
        mongo.db.create_collection("users", validator=USER_SCHEMA)
        mongo.db.create_collection("profile_views", validator=PROFILE_VIEW_SCHEMA)
        mongo.db.create_collection("likes", validator=LIKE_SCHEMA)
        
        # Unique indexes
        mongo.db.users.create_index("username", unique=True)
        mongo.db.users.create_index("email", unique=True)
        
        # Geospatial index for location
        mongo.db.users.create_index([("location", "2dsphere")])
        
        # Indexes for search and filtering
        mongo.db.users.create_index("interests")  
        mongo.db.users.create_index("gender")    
        mongo.db.users.create_index("sexual_preferences")
        mongo.db.users.create_index("fame_rating")
        mongo.db.users.create_index("online")    
        mongo.db.users.create_index("last_connection")
        
		# Indexes for profile views
        mongo.db.profile_views.create_index([("viewer_id", 1), ("viewed_id", 1)])
        mongo.db.profile_views.create_index("viewed_at")

        # Indexes for likes
        mongo.db.likes.create_index([("from_user_id", 1), ("to_user_id", 1)], unique=True)
        mongo.db.likes.create_index("created_at")

        print("Database initialized successfully")
        
    except Exception as e:
        if "already exists" not in str(e):
            print(f"Error initializing database: {e}")
            