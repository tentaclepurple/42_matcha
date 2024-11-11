from flask_pymongo import PyMongo

mongo = PyMongo()


USER_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "email", "password", "first_name", "last_name", "verified", "created_at"],
        "properties": {
            "_id": {
                "bsonType": "objectId",
                "description": "must be an ObjectId and is automatically generated"
            },
            # basic required fields
            "username": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "email": {
                "bsonType": "string",
                "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                "description": "must be a valid email address"
            },
            "password": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "first_name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "last_name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "verified": {
                "bsonType": "bool",
                "description": "email verification status"
            },
            "created_at": {
                "bsonType": "date",
                "description": "account creation date"
            },
            
            # status
            "online": {
                "bsonType": "bool",
                "description": "user online status"
            },
            "last_connection": {
                "bsonType": "date",
                "description": "last connection timestamp"
            },
            "profile_completed": {
                "bsonType": "bool",
                "description": "whether the profile is completed"
            },
            
            # profile
            "gender": {
                "enum": ["male", "female", "other"],
                "description": "user gender"
            },
            "sexual_preferences": {
                "bsonType": "array",
                "items": {
                    "enum": ["male", "female", "other"]
                },
                "description": "array of gender preferences"
            },
            "biography": {
                "bsonType": "string",
                "description": "user biography"
            },
            "interests": {
                "bsonType": "array",
                "items": {
                    "bsonType": "string"
                },
                "description": "array of interest tags"
            },
            "photos": {
                "bsonType": "array",
                "maxItems": 5,
                "items": {
                    "bsonType": "object",
                    "required": ["url", "is_profile"],
                    "properties": {
                        "url": {
                            "bsonType": "string"
                        },
                        "is_profile": {
                            "bsonType": "bool"
                        },
                        "uploaded_at": {
                            "bsonType": "date"
                        }
                    }
                }
            },
            "location": {
                "bsonType": "object",
                "required": ["type", "coordinates"],
                "properties": {
                    "type": {
                        "enum": ["Point"]
                    },
                    "coordinates": {
                        "bsonType": "array",
                        "minItems": 2,
                        "maxItems": 2,
                        "items": {
                            "bsonType": "double"
                        }
                    }
                }
            },
            "fame_rating": {
                "bsonType": "int",
                "minimum": 0,
                "description": "user popularity rating"
            },
            
            # Other
            "blocked_users": {
                "bsonType": "array",
                "items": {
                    "bsonType": "objectId"
                },
                "description": "array of blocked user IDs"
            }
        },
        "additionalProperties": False
    }
}


def init_db():
    """Crear colección con su estructura al iniciar el servidor"""
    try:
        # Crear la colección con validación
        mongo.db.create_collection("users", validator=USER_SCHEMA)
        
        # Índices únicos
        mongo.db.users.create_index("username", unique=True)
        mongo.db.users.create_index("email", unique=True)
        
        # Índice geoespacial
        mongo.db.users.create_index([("location", "2dsphere")])
        
        # Índices para búsquedas y filtros comunes
        mongo.db.users.create_index("interests")  
        mongo.db.users.create_index("gender")    
        mongo.db.users.create_index("sexual_preferences")
        mongo.db.users.create_index("fame_rating")
        mongo.db.users.create_index("online")    
        mongo.db.users.create_index("last_connection")
        
        print("Database initialized successfully")
        
    except Exception as e:
        if "already exists" not in str(e):
            print(f"Error initializing database: {e}")