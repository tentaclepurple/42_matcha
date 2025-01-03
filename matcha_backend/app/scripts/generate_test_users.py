# generate_test_users.py

import random
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo

from datetime import datetime, timedelta, timezone
import requests
UTC = timezone.utc

cities = [
    {'name': 'Madrid', 'coords': [-3.7038, 40.4168]},
    {'name': 'Barcelona', 'coords': [2.1734, 41.3851]},
    {'name': 'Valencia', 'coords': [-0.3763, 39.4699]},
    {'name': 'Seville', 'coords': [-5.9845, 37.3891]},
    {'name': 'Bilbao', 'coords': [-2.9253, 43.2630]},
    {'name': 'Barakaldo', 'coords': [-2.9899, 43.2972]},
    {'name': 'Leioa', 'coords': [-2.9869, 43.3329]},
    {'name': 'Portugalete', 'coords': [-3.0208, 43.3183]},
    {'name': 'Basauri', 'coords': [-2.8833, 43.2333]},
    {'name': 'Galdakao', 'coords': [-2.8417, 43.2333]},
    {'name': 'Sondika', 'coords': [-2.8975, 43.2833]},
    {'name': 'Mungia', 'coords': [-2.8333, 43.3500]},
    {'name': 'Basauri', 'coords': [-2.8833, 43.2333]},
    {'name': 'Urduliz', 'coords': [-3.0167, 43.3833]},
    {'name': 'Zamudio', 'coords': [-2.8667, 43.2833]},
    {'name': 'Derio', 'coords': [-2.8833, 43.2833]},
    {'name': 'Erandio', 'coords': [-2.9833, 43.3000]},
]


def generate_rand_location(index):
    # given a limited number of seeds, generate a random location
    city = cities[index % len(cities)]
    return [city['coords'][0] + random.uniform(-0.025, 0.025), city['coords'][1] + random.uniform(-0.025, 0.025)]


def generate_test_users(mongo, num_users=50):
    """Generate test users with complete profiles"""

    # Sample data pools
    interests = ["animals", "anime", "art", "astrology", "beauty", "blogging", "board games", 
        "camping", "cars", "collecting", "comedy", "cooking", "crafts", "cycling", 
        "dancing", "diy", "drinks", "fashion", "fishing", "fitness", "foodie", 
        "gaming", "gardening", "health", "hiking", "history", "investing", 
        "karaoke", "languages", "magic", "meditation", "movies", "music", 
        "nature", "nightlife", "partying", "photography", "podcasts", "politics", 
        "puzzles", "reading", "religion", "running", "science", "sex", "skating", 
        "skiing", "sports", "surfing", "swimming", "technology", "theater", 
        "traditions", "traveling", "volunteering", "writing", "yoga"]


    print("Creating test users...")

    response = requests.get(
        f'https://randomuser.me/api/?results={num_users}')
    if response.status_code != 200:
        print("Failed to fetch data from URL")
        return

    data = response.json()

    for i in range(num_users):
        user = data['results'][i]

        # Basic info
        user = {
            'username': user['login']['username'],
            'email': user['email'],
            'password': user['login']['sha256'],
            'first_name': user['name']['first'],
            'last_name': user['name']['last'],
            'age': random.randint(18, 30),
            'verified': True,
            'created_at': datetime.now(UTC) - timedelta(days=random.randint(1, 365)),
            'gender': user['gender'],
            'sexual_preferences': random.choice(['male', 'female', 'bisexual', 'other']),
            'biography': user['name']['first'] + " " + user['name']['last'] + " is a test user. We're sorry for not being able to provide more information. Maybe you can ask them directly?",
            'interests': random.sample(interests, random.randint(2, 5)),
            'photos': [
                {
                    'url': user['picture']['large'],
                    'is_profile': True,
                    'uploaded_at': datetime.now(UTC)
                }
            ],
            'location': {
                'type': 'Point',
                'coordinates':  generate_rand_location(i)
            },
            'online': random.choice([True, False]),
            'last_connection': datetime.now(UTC) - timedelta(minutes=random.randint(1, 1440)),
            'profile_completed': True,
            'fame_rating': random.randint(0, 100),
            'blocked_users': [],
            'reported': False
        }
        try:
            for interest in user['interests']:
                mongo.db.tags.update_one(
                    {"name": interest},
                    {"$inc": {"count": 1}},
                    upsert=True
                )
            mongo.db.users.insert_one(user)
            print(f"Created user: {user['username']}")
        except Exception as e:
            print(f"Error creating user {user['username']}: {str(e)}")
    print(f"Created {num_users} test users")
