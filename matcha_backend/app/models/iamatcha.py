# app/models/iamatcha.py


import google.generativeai as genai
from datetime import datetime
from bson import ObjectId
from ..config.database import mongo
from .chat import ChatModel
from .like import LikeModel
from .notification import NotificationModel
from .context import initial_message
from .bot_profiles import BOT_PROFILES
from dotenv import load_dotenv
import random
import os


load_dotenv()
KEY = os.getenv('GOOGLE_KEY')
model1 = 'gemini-1.5-flash'
model2 = 'gemini-1.5-flash-8b'
model3 = 'gemini-1.5-pro'
model_selection = model2



class BotModel:
   @classmethod
   def initialize_gemini(cls):
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
   def select_bot_for_user(cls, user_id: str):
       """Select a bot for the user based on their profile"""
       user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
       if not user:
           return None

       user_age = user.get('age', 25)
       user_interests = set(user.get('interests', []))
       user_gender = user.get('gender')
       user_preferences = user.get('sexual_preferences')

       scores = {}
       for bot_id, bot in BOT_PROFILES.items():
           score = 0
           bot_age = bot['age']
           print(f"\n**Bot {bot['username']}, User {user['username']}")

           difference = abs(user_age - bot_age)
           age_score = max(0.5, 12 - (difference / 2.5))
           print(f" user age: {user_age}, bot age: {bot_age}, age_score: {age_score}")
           score += age_score
           
           # common interests
           matching_interests = len(user_interests & set(bot['interests']))
           print(f" Matching interests: {matching_interests}")
           score += matching_interests * 2
           
           # gender and sexual preferences
           sex_score = 0
           if bot['sexual_preferences'] in [user_gender, "bisexual"] and user_preferences in [bot['gender'], "bisexual"]:
               sex_score = 15
               score += sex_score
           else:
               sex_score = -5
           print(f" bot sexual preferences: {bot['sexual_preferences']}, User sexual preferences: {user_preferences}, Sex_score = {sex_score}")

           scores[bot_id] = score
           print(f"-> Bot {bot['username']}: score {score}")   
       

       selected_bot = max(scores.items(), key=lambda x: x[1])[0]
       print(f"\nSelected: {BOT_PROFILES[selected_bot]['username']}")
       return BOT_PROFILES[selected_bot]

   @classmethod
   def check_and_create_bot(cls):
       """Create bot profiles if they don't exist"""
       for bot_data in BOT_PROFILES.values():
           if not mongo.db.users.find_one({"_id": bot_data["_id"]}):
               bot_profile = {
                   **bot_data,
                   "email": f"{bot_data['username'].lower()}@bot.com",
                   "password": "hash_seguro",
                   "verified": True,
                   "created_at": datetime.now(),
                   "online": True,
                   "profile_completed": True,
                   "photos": [
                       {
                           "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2swWp5UgJHG0IUxDq808p-JHNTCRzttQtKw&s",
                           "is_profile": True,
                           "uploaded_at": datetime.now()
                       }
                   ],
                   "fame_rating": 100
               }
               mongo.db.users.insert_one(bot_profile)

   @classmethod
   def get_user_context(cls, user_id: str) -> str:
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
   def get_conversation_history(cls, user_id: str, bot_id: str) -> dict:    
       bot = next((bot for bot in BOT_PROFILES.values() if str(bot["_id"]) == bot_id), None)
       if bot:
           bot_context = bot["context"]
       else:
           # Manejar el caso en el que el bot_id no se encuentre en BOT_PROFILES
           bot_context = ""
       conversation = mongo.db.conversations.find_one({
           "$or": [
               {"from_user_id": ObjectId(user_id), "to_user_id": ObjectId(bot_id)},
               {"from_user_id": ObjectId(bot_id), "to_user_id": ObjectId(user_id)}
           ]
       })
       
       if not conversation:
           conversation = {
               "from_user_id": ObjectId(user_id),
               "to_user_id": ObjectId(bot_id),
               "context": bot_context,
               "messages": [],
               "created_at": datetime.now(),
               "updated_at": datetime.now(),
               "status": "active"
           }
       introtext = cls
       return conversation

   @classmethod
   def save_conversation(cls, conversation: dict):
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
   def prepare_chat_history(cls, conversation: dict, bot_id: str, bot: dict) -> list:
        # Extraer información crítica
        critical_context = {
            "user_name": conversation.get("context", "").split("- Nombre: ")[1].split("\n")[0].strip(),
            "bot_name": bot["first_name"]
        }
        
        # Crear variaciones de recordatorios más naturales
        def create_natural_reminder():
            reminders = [
                f"[Contexto: Conversación entre {critical_context['bot_name']} y {critical_context['user_name']}]",
                f"[Mantener personalidad de {critical_context['bot_name']} y contexto con {critical_context['user_name']}]",
                f"[Continuar conversación natural con {critical_context['user_name']}]",
                f"[Mantener el tono y estilo establecido en la conversación]"
            ]
            return {
                "role": "user",
                "parts": [random.choice(reminders)]
            }
        
        chat_history = [{"role": "user", "parts": [conversation["context"]]}]
        
        # Obtener mensajes recientes
        recent_messages = conversation["messages"][-15:]
        
        # Insertar recordatorios sutiles cada ciertos mensajes
        for i, msg in enumerate(recent_messages):
            # Insertar recordatorio solo cada 7 mensajes para hacerlo menos frecuente
            if i % 7 == 0 and i > 0:  # Evitar el primero para no ser repetitivo
                chat_history.append(create_natural_reminder())
                
            role = "user" if msg["from_id"] != ObjectId(bot_id) else "model"
            chat_history.append({
                "role": role,
                "parts": [msg["content"]]
            })
        
        # Añadir un recordatorio final sutil
        chat_history.append({
            "role": "user",
            "parts": [f"[Mantener conversación natural como {critical_context['bot_name']}]"]
        })
        
        return chat_history

   @classmethod
   def handle_profile_completion(cls, user_id: str):
       try:
           selected_bot = cls.select_bot_for_user(user_id)
           if not selected_bot:
               return False
               
           bot_id = str(selected_bot["_id"])
           
           LikeModel.add_like(bot_id, user_id, "like")
           NotificationModel.create(
               user_id=user_id,
               type="like",
               from_user_id=bot_id
           )
           return True
       except Exception as e:
           print(f"Bot like error: {e}")
           return False
   
   @classmethod
   def get_context_with_intro(cls, bot):
       gender_map = {"male": "hombre", "female": "mujer"}
       preferences_map = {
               "male": "los hombres",
               "female": "las mujeres",
               "bisexual": "hombres y mujeres",
               "other": "otros géneros"
           }

       gender = gender_map.get(bot['gender'], bot['gender'])
       sexual = preferences_map.get(bot['sexual_preferences'])

       context_intro = f"""
           Información sobre ti:
           - Tu nombre es {bot['first_name']}
           - Tienes {bot['age']} años
           - Eres {gender}
           - Te atraen sexualmente {sexual}
           - Tus intereses son: {', '.join(bot['interests'])}
           - Una breve biografía adicional sobre ti: {bot['biography']}
            Y este es tu contexto de conversación ampliado:
           """
       return f"{context_intro}\n\n{bot['context']}"

   @classmethod
   def handle_user_like(cls, user_id: str, bot_id: str):
       try:
           model = cls.initialize_gemini()
           user_context = cls.get_user_context(user_id)
           conversation = cls.get_conversation_history(user_id, bot_id)

           if not model:
              print("Model not found")
           if not user_context:
              print("User context not found")
           if not conversation:
              print("Conversation not found")
           
           if not conversation["messages"]:
               bot = next((bot for bot in BOT_PROFILES.values() if str(bot["_id"]) == bot_id), None)
               if not bot:
                   print(f"No se encontró el bot con ID {bot_id}")
                   return False

               context = cls.get_context_with_intro(bot)

               conversation["context"] = f"{context}\n\n{user_context}"
               chat = model.start_chat(history=[{"role": "user", "parts": [conversation["context"]]}])
               response = chat.send_message(initial_message)
               
               conversation["messages"].append({
                   "from_id": ObjectId(bot_id),
                   "to_id": ObjectId(user_id),
                   "content": response.text.strip(),
                   "timestamp": datetime.now(),
                   "read": False
               })
               
               cls.save_conversation(conversation)
               
               ChatModel.send_message(
                   from_user_id=str(bot_id),
                   to_user_id=user_id,
                   content=response.text.strip(),
                   msg_type='text'
               )
           
           return True
       except Exception as e:
           print(f"Bot message error: {e}")
           return False


   @classmethod
   def handle_user_message(cls, user_id: str, message: str, bot_id: str):
       try:
           bot = next((bot for bot in BOT_PROFILES.values() if str(bot["_id"]) == bot_id), None)
           if not bot:
               return False
               
           conversation = cls.get_conversation_history(user_id, bot_id)
           
           conversation["messages"].append({
               "from_id": ObjectId(user_id),
               "to_id": ObjectId(bot_id),
               "content": message,
               "timestamp": datetime.now(),
               "read": False
           })
           
           context = cls.get_context_with_intro(bot)
           user_context = cls.get_user_context(user_id)
           conversation["context"] = f"{context}\n\n{user_context}"
           
           model = cls.initialize_gemini()
           chat_history = cls.prepare_chat_history(conversation, bot_id, bot)
           chat = model.start_chat(history=chat_history)
           
           response = chat.send_message(message)
           response_text = response.text.strip()
           
           conversation["messages"].append({
               "from_id": ObjectId(bot_id),
               "to_id": ObjectId(user_id),
               "content": response_text,
               "timestamp": datetime.now(),
               "read": False
           })
           
           cls.save_conversation(conversation)
           
           ChatModel.send_message(
               from_user_id=str(bot_id),
               to_user_id=user_id,
               content=response_text,
               msg_type='text'
           )
           
           return True
           
       except Exception as e:
           print(f"Bot response error: {e}")
           return False