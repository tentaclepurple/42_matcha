# MongoDB
MONGO_ROOT_USERNAME=root
MONGO_ROOT_PASSWORD=rootpassword
MONGO_DATABASE=matcha

# Mongo Express
ME_CONFIG_BASICAUTH_USERNAME=admin
ME_CONFIG_BASICAUTH_PASSWORD=adminpass

# Flask
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your_secret_key

#email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=matcha42urduliz@gmail.com
MAIL_PASSWORD=mktryfxjpafoeqcm




#ENDPOINTS

### http://localhost:5000/api/users/register

    {
        "username": "testuser",
        "email": "email@gmail.com",
        "password": "test123",
        "first_name": "Test",
        "last_name": "User"
    }
    sends email with verification link
    user follow the ling and verified=True


