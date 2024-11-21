# generate_test_users.py

import sys
import os
import random
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo

from datetime import datetime, timedelta, timezone
UTC = timezone.utc


# Load environment variables
load_dotenv()

# Create Flask app and configure MongoDB
app = Flask(__name__)

print("env vars:", os.getenv('MONGO_ROOT_USERNAME'), os.getenv('MONGO_ROOT_PASSWORD'), os.getenv('MONGO_DATABASE'))
app.config["MONGO_URI"] = (
    f"mongodb://{os.getenv('MONGO_ROOT_USERNAME')}:"
    f"{os.getenv('MONGO_ROOT_PASSWORD')}@localhost:27017/"
    f"{os.getenv('MONGO_DATABASE')}?authSource=admin"
)

mongo = PyMongo(app)

def generate_test_users(num_users=50):
    """Generate test users with complete profiles"""
    
    # Sample data pools
    usernames = [f"test_user_{i}" for i in range(num_users)]
    interests = ['music', 'movies', 'sports', 'reading', 'travel', 'food', 'art', 'gaming', 'fitness', 'technology']
    cities = [
        {'name': 'Madrid', 'coords': [-3.7038, 40.4168]},
        {'name': 'Barcelona', 'coords': [2.1734, 41.3851]},
        {'name': 'Valencia', 'coords': [-0.3763, 39.4699]},
        {'name': 'Seville', 'coords': [-5.9845, 37.3891]},
    ]
    
    with app.app_context():
        for i in range(num_users):
            # Basic info
            gender = random.choice(['male', 'female', 'other'])
            age = random.randint(18, 50)
            
            user = {
                'username': usernames[i],
                'email': f"test{i}@test.com",
                'password': 'hashedPassword123',
                'first_name': f"FirstName{i}",
                'last_name': f"LastName{i}",
                'age': age,
                'verified': True,
                'created_at': datetime.now(UTC) - timedelta(days=random.randint(1, 365)),
                
                'gender': gender,
                'sexual_preferences': random.choice(['male', 'female', 'bisexual', 'other']),
                'biography': f"Bio for test user {i}",
                'interests': random.sample(interests, random.randint(2, 5)),
                'photos': [
                    {
                        'url': f"/static/test/photo{j}.jpg",
                        'is_profile': j == 0,
                        'uploaded_at': datetime.now(UTC)
                    } for j in range(random.randint(1, 5))
                ],
                
                'location': {
                    'type': 'Point',
                    'coordinates': random.choice(cities)['coords']
                },
                
                'online': random.choice([True, False]),
                'last_connection': datetime.now(UTC) - timedelta(minutes=random.randint(1, 1440)),
                'profile_completed': True,
                'fame_rating': random.randint(0, 100),
                'blocked_users': [],
                'reported': False
            }
            
            try:
                mongo.db.users.insert_one(user)
                print(f"Created user: {user['username']}")
            except Exception as e:
                print(f"Error creating user {user['username']}: {str(e)}")
                
    print(f"Created {num_users} test users")

if __name__ == "__main__":
    generate_test_users(50)