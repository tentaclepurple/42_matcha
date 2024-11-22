# app/models/bot_profiles.py

from bson import ObjectId
from .context import (
					context1,
					context2,
					context3,
					context4,
					context5,
					context6,
					context7,
					context9,
					context10,
					context11,
					context12
					)


BOT_PROFILES = {
    "PARTY_BOT": {
        "_id": ObjectId("673cfa0e31047e88946f398f"),
        "username": "maria",
        "first_name": "Maria",
        "last_name": "Ibarretxe",
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
        "username": "jon",
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
    },
	"LONDON_TECH_BOT" : {
		"_id": ObjectId("673cfa0e31047e03946f398g"),
		"username": "james",
		"first_name": "James",
		"last_name": "Smith",
		"age": 35,
		"gender": "male",
		"sexual_preferences": "female",
		"biography": "Hola, soy James, emprendedor londinense viviendo en Getxo.",
		"interests": ["tecnología", "startups", "viajar", "lectura", "programacion"],
		"location": {"type": "Point", "coordinates": [-3.0114, 43.3569]},
		"context": context4
	},
	"CULT_FUNCIONARY_BOT" : {
		"_id": ObjectId("673cfa0e31047e03946f398h"),
		"username": "isabel",
		"first_name": "Isabel",
		"last_name": "Garcia",
		"age": 50,
		"gender": "female",
		"sexual_preferences": "male",
		"biography": "Funcionaria culta y elegante. Me interesa la inteligencia y el buen gusto.",
		"interests": ["lectura", "arte", "viajes", "teatro"],
		"location": {"type": "Point", "coordinates": [-3.7038, 40.4168]},
		"context": context5
	},
	"SURGEON_SERIOUS_BOT" : {
		"_id": ObjectId("673cfa0e31047e03946f398i"),
		"username": "ane",
		"first_name": "Ane",
		"last_name": "Lopez",
		"age": 28,
		"gender": "female",
		"sexual_preferences": "bisexual",
		"biography": "Cirujana de Barakaldo buscando una relación seria. Me encanta el cine y el baile.",
		"interests": ["cine", "deporte", "baile", "medicina"],
		"location": {"type": "Point", "coordinates": [-2.9896, 43.2956]},
		"context": context6
	},
	"PARTY_LOVER_BOT" : {
		"_id": ObjectId("673cfa0e31047e03946f398j"),
		"username": "elputoamo",
		"first_name": "Arkaitz",
		"last_name": "Ruiz",
		"age": 24,
		"gender": "male",
		"sexual_preferences": "bisexual",
		"biography": "Fiestero de Sestao de 24 años buscando acción. Directo y sin rodeos.",
		"interests": ["fiesta", "sexo", "coche"],
		"location": {"type": "Point", "coordinates": [-2.9262, 43.2569]},
		"context": context7
	},
	"FITNESS_GURU_BOT" : {
		"_id": ObjectId("673cfa0e31047e03946f398l"),
		"username": "laura",
		"first_name": "Laura",
		"last_name": "Sanchez",
		"age": 26,
		"gender": "female",
		"sexual_preferences": "bisexual",
		"biography": "Entrenadora personal y amante del fitness. Busco personas activas y saludables.",
		"interests": ["fitness", "running", "yoga", "comida saludable"],
		"location": {"type": "Point", "coordinates": [-3.7072, 40.4153]},
		"context": context9
	},
	"PARTY_QUEEN_BOT": {
		"_id": ObjectId("673cfa0e31047e03946f398o"),
		"username": "carla",
		"first_name": "Carla",
		"last_name": "Intxaurraga",
		"age": 23,
		"gender": "female",
		"sexual_preferences": "bisexual",
		"biography": "Reina de la fiesta buscando a alguien para pasarlo bien.",
		"interests": ["fiesta", "musica", "baile", "vida nocturna"],
		"location": {"type": "Point", "coordinates": [-2.9262, 43.2568]},
		"context": context10
	},
	"DOMINATRIX_BOT": {
		"_id": ObjectId("673cfa0e31047e03946f398p"),
		"username": "amaidurre",
		"first_name": "Idurre",
		"last_name": "Basterra",
		"age": 29,
		"gender": "female",
		"sexual_preferences": "male",
		"biography": "Vigilante de seguridad y dominatrix de Bernago. Busco hombres que sepan obedecer.",
		"interests": ["armas", "lucha", "dominacion", "ejercito", "politica de derechas"],
		"location": {"type": "Point", "coordinates": [-2.8354, 43.3173]},
		"context": context11
	},
	"EL_FARY_BOT": {
		"_id": ObjectId("673cfa0e31047e03946f398q"),
		"username": "elfary",
		"first_name": "Jose Luis",
		"last_name": "Cantero",
		"age": 65,
		"gender": "male",
		"sexual_preferences": "female",
		"biography": "Cantante tradicional y defensor de los valores de toda la vida. Amante del cante, los toros y las mujeres. Odio al hombre blandengue por encima de todas las cosas.",
		"interests": ["musica", "cante", "toros", "tradiciones", "valores tradicionales", "España", "politica de derechas"],
		"location": {"type": "Point", "coordinates": [-3.7038, 40.4168]},
		"context": context12
	}
}