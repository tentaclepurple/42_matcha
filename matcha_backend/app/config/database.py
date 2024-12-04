# app/config/database.py


from flask_pymongo import PyMongo
from .schemas import *

mongo = PyMongo()


def init_db():
    """Create the database collections with validation and indexes."""
    try:
        collections_to_create = {
            "users": USER_SCHEMA,
            "profile_views": PROFILE_VIEW_SCHEMA,
            "likes": LIKE_SCHEMA,
            "tags": TAG_SCHEMA,
            "notifications": NOTIFICATION_SCHEMA,
            "chat_messages": CHAT_MESSAGE_SCHEMA,
            "conversations": CONVERSATION_SCHEMA
        }

        # Create COLLECTIONS if they don't exist
        existing_collections = mongo.db.list_collection_names()
        
        for name, schema in collections_to_create.items():
            if name not in existing_collections:
                print(f"Creating collection: {name}")
                mongo.db.create_collection(name, validator=schema)
        
        # INDEXES
        # Unique indexes for users
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
        mongo.db.users.create_index("profile_completed")
        
		# Login attempts monitoring indexes
        mongo.db.users.create_index([
            ("locked_until", 1),
            ("login_attempts", 1)
        ], sparse=True)

        # Indexes for profile views
        mongo.db.profile_views.create_index([("viewer_id", 1), ("viewed_id", 1)])
        mongo.db.profile_views.create_index([("viewed_id", 1), ("viewed_at", -1)])
        mongo.db.profile_views.create_index("viewed_at")

        # Indexes for likes
        mongo.db.likes.create_index("created_at")
        mongo.db.likes.create_index([("from_user_id", 1), ("to_user_id", 1), ("type", 1)])
        mongo.db.likes.create_index([("to_user_id", 1), ("type", 1)])

        # Indexes for tags
        mongo.db.tags.create_index("name", unique=True)
        
        # Indexes for notifications
        mongo.db.notifications.create_index([("user_id", 1), ("read", 1)])
        mongo.db.notifications.create_index([("user_id", 1), ("created_at", -1)])
        mongo.db.notifications.create_index("from_user_id")
        
        # Indexes for chat messages
        mongo.db.chat_messages.create_index([
            ("from_user_id", 1), ("to_user_id", 1), ("created_at", -1)
            ])
        mongo.db.chat_messages.create_index([
            ("to_user_id", 1), ("read", 1)
            ])
        mongo.db.chat_messages.create_index("created_at")

        # Indexes for conversations
        mongo.db.conversations.create_index([
                ("from_user_id", 1),
                ("to_user_id", 1),
                ("updated_at", -1)
            ])

        mongo.db.conversations.create_index([
            ("messages.timestamp", -1)
        ])

        print("Database initialized successfully")
        
    except Exception as e:
        if "already exists" not in str(e):
            print(f"Error initializing database: {e}")
            