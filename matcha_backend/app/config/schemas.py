# app/config/schemas.py


USER_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "email", "password", "first_name", "last_name", "age", "verified", "created_at"],
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
			"age": {
				"bsonType": "int",
				"minimum": 18,
				"description": "must be an integer >= 18 and is required"
			},
            "verified": {
                "bsonType": "bool",
                "description": "email verification status"
            },
            "created_at": {
                "bsonType": "date",
                "description": "account creation date"
            },
			# Login attempts tracking
            "login_attempts": {
                "bsonType": "int",
                "minimum": 0,
                "description": "number of failed login attempts"
            },
            "last_failed_login": {
                "bsonType": ["date", "null"],
                "description": "timestamp of last failed login attempt"
            },
            "locked_until": {
                "bsonType": ["date", "null"],
                "description": "account locked until this timestamp"
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
                "enum": ["male", "female", "bisexual", "other", None],
                "description": "gender preferences"
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
            },
            "context": {
                "bsonType": ["string", "null"],
                "description": "ia context"
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


TAG_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "count"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "tag name (without #)"
            },
            "count": {
                "bsonType": "int",
                "description": "number of users using this tag"
            }
        }
    }
}


NOTIFICATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "type", "created_at", "read"],
        "properties": {
            "_id": {
                "bsonType": "objectId"
            },
            "user_id": {
                "bsonType": "objectId",
                "description": "User who receives the notification"
            },
            "from_user_id": {
                "bsonType": "objectId",
                "description": "User who triggered the notification"
            },
            "type": {
                "enum": ["profile_view", "like", "unlike", "match", "message"],
                "description": "Type of notification"
            },
            "created_at": {
                "bsonType": "date",
                "description": "When the notification was created"
            },
            "read": {
                "bsonType": "bool",
                "description": "Whether the notification has been read"
            }
        },
        "additionalProperties": False
    }
}


CHAT_MESSAGE_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["from_user_id", "to_user_id", "content", "type", "created_at", "read"],
        "properties": {
            "_id": {
                "bsonType": "objectId"
            },
            "from_user_id": {
                "bsonType": "objectId",
                "description": "ID of the user sending the message"
            },
            "to_user_id": {
                "bsonType": "objectId",
                "description": "ID of the user receiving the message"
            },
            "content": {
                "bsonType": "string",
                "description": "Message content or image URL"
            },
            "type": {
                "enum": ["text", "image"],
                "description": "Type of message"
            },
            "created_at": {
                "bsonType": "date",
                "description": "When the message was sent"
            },
            "read": {
                "bsonType": "bool",
                "description": "Whether the message has been read"
            }
        },
        "additionalProperties": False
    }
}


CONVERSATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["from_user_id", "to_user_id", "context", "messages", "created_at", "updated_at"],
        "properties": {
            "_id": {
                "bsonType": "objectId"
            },
            "from_user_id": {
                "bsonType": "objectId"
            },
            "to_user_id": {
                "bsonType": "objectId"
            },
            "context": {
                "bsonType": "string"
            },
            "messages": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["from_id", "to_id", "content", "timestamp", "read"],
                    "properties": {
                        "from_id": {
                            "bsonType": "objectId"
                        },
                        "to_id": {
                            "bsonType": "objectId"
                        },
                        "content": {
                            "bsonType": "string"
                        },
                        "timestamp": {
                            "bsonType": "date"
                        },
                        "read": {
                            "bsonType": "bool"
                        }
                    }
                }
            },
            "created_at": {
                "bsonType": "date"
            },
            "updated_at": {
                "bsonType": "date"
            },
            "status": {
                "enum": ["active", "archived", "blocked"]
            }
        }
    }
}
