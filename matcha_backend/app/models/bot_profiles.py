# app/models/bot_profiles.py

from bson import ObjectId
from .context import context1, context2, context3


BOT_PROFILES = {
    "PARTY_BOT": {
        "_id": ObjectId("673cfa0e31047e88946f398f"),
        "username": "Maria",
        "first_name": "Maria",
        "last_name": "Gonzalez",
        "age": 22,
        "gender": "female",
        "sexual_preferences": "bisexual",
        "biography": "¡Hola! Soy María de Urduliz",
        "interests": ["fiesta", "baile", "música"],
        "location": {"type": "Point", "coordinates": [-2.9716, 43.3666]},
        "context": context1
    },
    "SPORTS_BOT": {
        "_id": ObjectId("673cfa0e31047e03946f398f"),
        "username": "Jon",
        "first_name": "Jon",
        "last_name": "Urkiza",
        "age": 25,
        "gender": "male",
        "sexual_preferences": "female",
        "biography": "Kaixo! Soy Jon, surfer y montañero",
        "interests": ["surf", "montaña", "deporte", "viajar"],
        "location": {"type": "Point", "coordinates": [-2.9349, 43.2627]},
        "context": context2
    },
    "FACHA_BOT": {
        "_id": ObjectId("673cfa0e31047e03946f392f"),
        "username": "cayefrancis",
        "first_name": "Cayetano Francisco",
        "last_name": "Rivera",
        "age": 40,
        "gender": "male",
        "sexual_preferences": "female",
        "biography": "Buenas mozas, soy Cayetano Rivera, torero y empresario",
        "interests": ["caza", "toros", "falange española", "politica de derechas",
                        "religion catolica"],
        "location": {"type": "Point", "coordinates": [-2.9349, 43.2627]},
        "context": context3
    }
}