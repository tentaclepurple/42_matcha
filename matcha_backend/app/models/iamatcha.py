# app/models/iamatcha.py

import google.generativeai as genai
from datetime import datetime
from bson import ObjectId
from ..config.database import mongo
from .chat import ChatModel
from .like import LikeModel
from .notification import NotificationModel
from .context import context1, initial_message
from dotenv import load_dotenv
import os

load_dotenv()

KEY = os.getenv('GOOGLE_KEY')
model_selection = 'gemini-1.5-flash-8b'

class BotModel:
    BOT_ID = ObjectId("673cfa0e31047e88946f398f")
    
    @classmethod
    def initialize_gemini(cls):
        """Initialize the Gemini model"""
        genai.configure(api_key=KEY)
        
        generation_config = {
            'temperature': 0.9,
            'top_p': 0.9,
            'top_k': 40,
            'max_output_tokens': 300,
            'candidate_count': 1
        }
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        return genai.GenerativeModel(
            model_name=model_selection,
            generation_config=generation_config,
            safety_settings=safety_settings
        )

    @classmethod
    def get_user_context(cls, user_id: str) -> str:
        """Get user context information"""
        try:
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if not user:
                return ""
            
            gender_map = {"male": "hombre", "female": "mujer"}
            preferences_map = {
                "male": "los hombres",
                "female": "las mujeres",
                "bisexual": "hombres y mujeres",
                "other": "otros géneros"
            }

            gender = gender_map.get(user.get('gender', ''), user.get('gender', ''))
            sexual = preferences_map.get(user.get('sexual_preferences', ''), 'otros géneros')

            user_context = f"""
            Información adicional del usuario con el que hablas:
            - Nombre: {user.get('first_name', '')}
            - Edad: {user.get('age', '')} años
            - Género: {gender}
            - Le atraen sexualmente {sexual}
            - Intereses: {', '.join(user.get('interests', []))}
            - Localización: {user.get('location', {}).get('coordinates', []) if user.get('location') else 'No disponible'}
            - Biografía: {user.get('biography', '')}
            """
            
            return user_context
            
        except Exception as e:
            print(f"Error getting user context: {e}")
            return ""

    @classmethod
    def get_conversation_history(cls, user_id: str) -> dict:
        """Get or create conversation history"""
        conversation = mongo.db.conversations.find_one({
            "$or": [
                {"from_user_id": ObjectId(user_id), "to_user_id": cls.BOT_ID},
                {"from_user_id": cls.BOT_ID, "to_user_id": ObjectId(user_id)}
            ]
        })
        
        if not conversation:
            conversation = {
                "from_user_id": ObjectId(user_id),
                "to_user_id": cls.BOT_ID,
                "context": context1,
                "messages": [],
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "status": "active"
            }
            
        return conversation

    @classmethod
    def save_conversation(cls, conversation: dict):
        """Save or update conversation"""
        conversation["updated_at"] = datetime.now()
        
        mongo.db.conversations.update_one(
            {
                "$or": [
                    {"from_user_id": conversation["from_user_id"], "to_user_id": conversation["to_user_id"]},
                    {"from_user_id": conversation["to_user_id"], "to_user_id": conversation["from_user_id"]}
                ]
            },
            {"$set": conversation},
            upsert=True
        )

    @classmethod
    def prepare_chat_history(cls, conversation: dict) -> list:
        """Prepare chat history for Gemini"""
        chat_history = [{"role": "user", "parts": [conversation["context"]]}]
        
        for msg in conversation["messages"]:
            role = "user" if msg["from_id"] != cls.BOT_ID else "model"
            chat_history.append({
                "role": role,
                "parts": [msg["content"]]
            })
        
        return chat_history

    @classmethod
    def check_and_create_bot(cls):
        """Create bot user if not exists"""
        if not mongo.db.users.find_one({"_id": cls.BOT_ID}):
            bot_data = {
                "_id": cls.BOT_ID,
                "username": "Maria",
                "email": "maria@bot.com",
                "password": "hash_seguro",
                "first_name": "Maria",
                "last_name": "Bot",
                "age": 22,
                "gender": "female",
                "sexual_preferences": "bisexual",
                "biography": "¡Hola! Soy María de Urduliz",
                "verified": True,
                "created_at": datetime.now(),
                "online": True,
                "profile_completed": True,
                "interests": ["fiesta", "baile", "música"],
                "photos": [
                    {
                        "url": "url_de_foto",
                        "is_profile": True,
                        "uploaded_at": datetime.now()
                    }
                ],
                "location": {
                    "type": "Point",
                    "coordinates": [-2.9716, 43.3666]  # Urduliz
                },
                "fame_rating": 100
            }
            mongo.db.users.insert_one(bot_data)

    @classmethod
    def handle_profile_completion(cls, user_id: str):
        """Like and start conversation with user"""
        try:
            # like user
            LikeModel.add_like(str(cls.BOT_ID), user_id, "like")
            
            # Create notification
            NotificationModel.create(
                user_id=user_id,
                type="like",
                from_user_id=str(cls.BOT_ID)
            )
            
            return True
        except Exception as e:
            print(f"Bot like error: {e}")
            return False

    @classmethod
    def handle_user_like(cls, user_id: str):
        """Handle user like and start conversation"""
        try:
            # Initialize chat
            model = cls.initialize_gemini()
            
            # Get user context and conversation
            user_context = cls.get_user_context(user_id)
            conversation = cls.get_conversation_history(user_id)
            
            # Add context to conversation if new
            if not conversation["messages"]:
                conversation["context"] = f"{context1}\n\n{user_context}"
                
                # Create initial message
                chat = model.start_chat(history=[{"role": "user", "parts": [conversation["context"]]}])
                response = chat.send_message(initial_message)
                
                # Save bot's initial message
                conversation["messages"].append({
                    "from_id": cls.BOT_ID,
                    "to_id": ObjectId(user_id),
                    "content": response.text.strip(),
                    "timestamp": datetime.now(),
                    "read": False
                })
                
                # Save conversation
                cls.save_conversation(conversation)
                
                # Send message through chat system
                ChatModel.send_message(
                    from_user_id=str(cls.BOT_ID),
                    to_user_id=user_id,
                    content=response.text.strip(),
                    msg_type='text'
                )
            
            return True
        except Exception as e:
            print(f"Bot message error: {e}")
            return False

    @classmethod
    def handle_user_message(cls, user_id: str, message: str):
        """Process user message and send response"""
        try:
            # Get conversation history
            conversation = cls.get_conversation_history(user_id)
            
            # Add user message
            conversation["messages"].append({
                "from_id": ObjectId(user_id),
                "to_id": cls.BOT_ID,
                "content": message,
                "timestamp": datetime.now(),
                "read": False
            })
            
            # Get user context
            user_context = cls.get_user_context(user_id)
            conversation["context"] = f"{context1}\n\n{user_context}"
            
            # Initialize model
            model = cls.initialize_gemini()
            
            # Prepare and start chat
            chat_history = cls.prepare_chat_history(conversation)
            chat = model.start_chat(history=chat_history)
            
            # Get response
            response = chat.send_message(message)
            response_text = response.text.strip()
            
            # Add bot response to conversation
            conversation["messages"].append({
                "from_id": cls.BOT_ID,
                "to_id": ObjectId(user_id),
                "content": response_text,
                "timestamp": datetime.now(),
                "read": False
            })
            
            # Save conversation
            cls.save_conversation(conversation)
            
            # Send through chat system
            ChatModel.send_message(
                from_user_id=str(cls.BOT_ID),
                to_user_id=user_id,
                content=response_text,
                msg_type='text'
            )
            
            return True
            
        except Exception as e:
            print(f"Bot response error: {e}")
            return False
