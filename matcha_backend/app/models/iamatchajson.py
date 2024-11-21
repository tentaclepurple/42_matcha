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
import json
import os
from pathlib import Path


load_dotenv()

KEY = os.getenv('GOOGLE_KEY')
model1 = 'gemini-1.5-flash'
model2 = 'gemini-1.5-flash-8b'
model3 = 'gemini-1.5-pro'

model_selection = model2


def load_chat_history(context):
    """Load chat history if exists"""
    history_file = Path('chat_history.json')
    if history_file.exists():
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "context": context,
        "messages": []
    }

def save_chat_history(history):
    """Save chat history"""
    with open('chat_history.json', 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


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
    def prepare_chat_history(cls, messages, user_id: str) -> list:
        """Convert chat messages to chat history format"""
        chat_history = [{"role": "user", "parts": [context1]}]  # Contexto base
        
        for msg in messages:
            role = "user" if str(msg['from_user_id']) == user_id else "model"
            chat_history.append({
                "role": role,
                "parts": [msg['content']]
            })
        
        return chat_history

    @classmethod
    def get_user_context(cls, user_id: str) -> str:
        """Get user context information"""
        try:
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if not user:
                return ""
            
            if user.get('gender') == "male":
                gender = "hombre"
            elif user.get('gender') == "female":
                gender = "mujer"
            
            if user.get('sexual_preferences') == "male":
                sexual = "los hombres"
            elif user.get('sexual_preferences') == "female":
                sexual = "las mujeres"
            elif user.get('sexual_preferences') == "bisexual":
                sexual = "hombres y mujeres"
            else:
                sexual = "otros generos"


            user_context = f"""
            Información adicional del usuario con el que hablas:
            - Nombre: {user.get('first_name', '')}
            - Edad: {user.get('age', '')} años
            - Género: {user.get('gender', '')}
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
            
            # Get user context
            user_context = cls.get_user_context(user_id)
            full_context = f"{context1}\n\n{user_context}"
            
            history = load_chat_history(full_context)

            chat_history = [{"role": "user", "parts": [history["context"]]}]
            for msg in history["messages"]:
                chat_history.append({
                    "role": "user" if msg["role"] == "user" else "model",
                    "parts": [msg["content"]]
                })
            
            chat = model.start_chat(history=chat_history)

            if not history["messages"]:
                response = chat.send_message(full_context + initial_message)
                
                history["messages"].append({
                        "role": "assistant",
                        "content": response.text
                    })
            
                save_chat_history(history)
            
            # send message to user
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
            # Get user data
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            
            # Get user context
            user_context = cls.get_user_context(user_id)
            full_context = f"{context1}\n\n{user_context}"
            history = load_chat_history(full_context)
            
            # Initialize model
            model = cls.initialize_gemini()
           
            chat_history = [{"role": "user", "parts": [history["context"]]}]
            for msg in history["messages"]:
                chat_history.append({
                    "role": "user" if msg["role"] == "user" else "model",
                    "parts": [msg["content"]]
                    })  
            
            chat = model.start_chat(history=chat_history)

            history["messages"].append({
                "role": "user",
                "content": message
            })

            response = chat.send_message(message)
            response_text = response.text.strip()

            history["messages"].append({
                "role": "assistant",
                "content": response_text
            })
            
            # Save chat history
            ChatModel.send_message(
                from_user_id=str(cls.BOT_ID),
                to_user_id=user_id,
                content=response_text,
                msg_type='text'
            )
            
            save_chat_history(history)

            return True
            
        except Exception as e:
            print(f"Bot response error: {e}")
            return False

    