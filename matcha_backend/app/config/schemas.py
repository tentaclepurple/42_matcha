# app/config/schemas.py


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
                "enum": ["male", "female", "other", None],
                "description": "user gender"
            },
            "sexual_preferences": {
                "bsonType": "array",
                "items": {
                    "enum": ["male", "female", "bisexual", None]
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
                "bsonType": ["object", "null"],
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
                "bsonType": ["array", "null"],
                "items": {
                    "bsonType": "objectId"
                },
                "description": "array of blocked user IDs"
            },
            "reported": {
                "bsonType": "bool",
                "description": "whether the user has been reported as fake"
            }
        },
        "additionalProperties": False
    }
}


PROFILE_VIEW_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["viewer_id", "viewed_id", "viewed_at"],
        "properties": {
            "_id": {
                "bsonType": "objectId"
            },
            "viewer_id": {
                "bsonType": "objectId",
                "description": "ID of the user who viewed the profile"
            },
            "viewed_id": {
                "bsonType": "objectId",
                "description": "ID of the user whose profile was viewed"
            },
            "viewed_at": {
                "bsonType": "date",
                "description": "When the profile was viewed"
            }
        },
        "additionalProperties": False
    }
}


LIKE_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["from_user_id", "to_user_id", "created_at", "type"],
        "properties": {
            "_id": {
                "bsonType": "objectId"
            },
            "from_user_id": {
                "bsonType": "objectId",
                "description": "ID of the user who gave the like/unlike"
            },
            "to_user_id": {
                "bsonType": "objectId",
                "description": "ID of the user who received the like/unlike"
            },
            "created_at": {
                "bsonType": "date",
                "description": "When the interaction happened"
            },
            "type": {
                "enum": ["like", "unlike"],
                "description": "Type of interaction: like or unlike"
            }
        },
        "additionalProperties": False
    }
}
