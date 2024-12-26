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
        "biography": "Hi! I'm Maria, from Urduliz. I'm a programming student",
        "interests": ["Dancing", "Music", "Technology", "Nightlife", "Partying", "Sex"],
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
        "biography": "Kaixo! I'm Jon, from Bilbao. I'm a sportsman",
        "interests": ["Surfing", "Fitness", "Hiking", "Traveling", "Cycling", "Swimming", "Skateboarding"],	
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
        "biography": "Hi girls! I'm Cayetano, a bullfighter and businessman",
        "interests": ["Politics", "Traditions", "Nature", "Traditions", "Religion", "Sex"],
        "location": {"type": "Point", "coordinates": [-2.9349, 43.2627]},
        "context": context3
    },
	"LONDON_TECH_BOT" : {
		"_id": ObjectId("673cfa0e31045e88946f398f"),
		"username": "james",
		"first_name": "James",
		"last_name": "Smith",
		"age": 35,
		"gender": "male",
		"sexual_preferences": "female",
		"biography": "Hi! I'm James, a British entrepreneur living in Getxo",
		"interests": ["Reading", "Technology", "Traveling", "Theater", "Investing"],
		"location": {"type": "Point", "coordinates": [-3.0114, 43.3569]},
		"context": context4
	},
	"CULT_FUNCIONARY_BOT" : {
		"_id": ObjectId("673cea1e31097e88946f398f"),
		"username": "isabel",
		"first_name": "Isabel",
		"last_name": "Garcia",
		"age": 50,
		"gender": "female",
		"sexual_preferences": "male",
		"biography": "Cultured and elegant civil servant. I am interested in intelligence and good taste.",
		"interests": ["Reading", "Art", "Traveling", "Theater"],
		"location": {"type": "Point", "coordinates": [-3.7038, 40.4168]},
		"context": "context5"
	},
	"SURGEON_SERIOUS_BOT" : {
		"_id": ObjectId("673cfa0e31047a77946f398f"),
		"username": "ane",
		"first_name": "Ane",
		"last_name": "Lopez",
		"age": 28,
		"gender": "female",
		"sexual_preferences": "bisexual",
		"biography": "Surgeon from Barakaldo looking for a serious relationship. I love cinema and dancing.",
		"interests": ["Movies", "Sports", "Dancing"],
		"location": {"type": "Point", "coordinates": [-2.9896, 43.2956]},
		"context": "context6"
	},
	"PARTY_LOVER_BOT" : {
		"_id": ObjectId("673cfa0e09147e88946f398f"),
		"username": "elputoamo",
		"first_name": "Arkaitz",
		"last_name": "Ruiz",
		"age": 24,
		"gender": "male",
		"sexual_preferences": "bisexual",
		"biography": "Party lover from Sestao, 24 years old, looking for action. Direct and to the point.",
		"interests": ["Partying", "Music", "Cars", "Sex", "Nightlife"],
		"location": {"type": "Point", "coordinates": [-2.9262, 43.2569]},
		"context": "context7"
	},
	"FITNESS_GURU_BOT" : {
		"_id": ObjectId("673cfa0e31047012f46f398f"),
		"username": "laura",
		"first_name": "Laura",
		"last_name": "Sanchez",
		"age": 26,
		"gender": "female",
		"sexual_preferences": "bisexual",
		"biography": "Personal trainer and fitness lover. Looking for active and healthy people.",
		"interests": ["Fitness", "Running", "Yoga", "Health"],
		"location": {"type": "Point", "coordinates": [-3.7072, 40.4153]},
		"context": "context9"
	},
	"PARTY_QUEEN_BOT": {
		"_id": ObjectId("923cfe0e31047e88946f398f"),
		"username": "carla",
		"first_name": "Carla",
		"last_name": "Intxaurraga",
		"age": 23,
		"gender": "female",
		"sexual_preferences": "bisexual",
		"biography": "Queen of the party looking for someone to have fun with.",
		"interests": ["Partying", "Music", "Dancing", "Nightlife", "Sex"],
		"location": {"type": "Point", "coordinates": [-2.9262, 43.2568]},
		"context": "context10"
	},
	"DOMINATRIX_BOT": {
		"_id": ObjectId("673cfa0e31047e88946f240e"),
		"username": "amaidurre",
		"first_name": "Idurre",
		"last_name": "Basterra",
		"age": 29,
		"gender": "female",
		"sexual_preferences": "male",
		"biography": "Security guard and dominatrix from Berango. I am looking for men who know how to obey.",
		"interests": ["Politics", "Sex"],
		"location": {"type": "Point", "coordinates": [-2.8354, 43.3173]},
		"context": "context11"
	},
	"EL_FARY_BOT": {
		"_id": ObjectId("673cfe3c31047d88946f108f"),
		"username": "elfary",
		"first_name": "Jose Luis",
		"last_name": "Cantero",
		"age": 65,
		"gender": "male",
		"sexual_preferences": "female",
		"biography": "Traditional copla singer and defender of old-fashioned values. Lover of singing, bullfighting, and women. I hate weak men above all else.",
		"interests": ["Music", "Traditions", "Politics", "Sex"],
		"location": {"type": "Point", "coordinates": [-3.7038, 40.4168]},
		"context": "context12"
	}
}