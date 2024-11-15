## MongoDB
MONGO_ROOT_USERNAME=root
MONGO_ROOT_PASSWORD=rootpassword
MONGO_DATABASE=matcha

## Mongo Express
ME_CONFIG_BASICAUTH_USERNAME=admin
ME_CONFIG_BASICAUTH_PASSWORD=adminpass

## Flask
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your_secret_key

## email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=matcha42urduliz@gmail.com
MAIL_PASSWORD=mktryfxjpafoeqcm

<br><br>


# ENDPOINTS

## http://localhost:5000/api/users/register

    {
        "username": "testuser",
        "email": "email@gmail.com",
        "password": "test123",
        "first_name": "Test",
        "last_name": "User"
    }
sends email with verification link
user follow the ling and verified=True

    return:

    {
    "message": "User registered successfully. Please check your email to verify your account.",
    "user_id": "6735c74739e2fdd44cc4479b"
    }
<br>

## http://localhost:5000/api/users/login

    {
    "username": "testusder",
    "password": "test123"
    }
turns connected to true

    returns:

    200 OK
    {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTU4MjQ0MiwianRpIjoiMTgzOWY0YWMtMzVhYy00YzgwLWFhZTAtNjE2OGVhY2ZmYjhjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY3MzVjNzQ3MzllMmZkZDQ0Y2M0NDc5YiIsIm5iZiI6MTczMTU4MjQ0MiwiY3NyZiI6ImM2ZDFlMDFjLWZhZjUtNDU3Yi1iZGI3LTdkNGUyOTc0MDBiMyIsImV4cCI6MTczMTU4NjA0Mn0.vIxb4P7O_7nlgStEfdX21YifPzLe8UMHO3rdXIMZqmU",
    "user": {
        "profile_completed": false,
        "user_id": "6735c74739e2fdd44cc4479b"
        }
    }
<br>

    400
    {
    "error": "Username and password are required"
    }
<br>


    401
    {
    "error": "Invalid credentials"
    }
<br>
    401
    {
    "error": "Email not verified"
    }

    // Ejemplo de petición en el frontend

    fetch('http://localhost:5000/api/users/profile', {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
<br>

 ## http://localhost:5000/api/users/logout
    
    header:

    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTU5Njg2MSwianRpIjoiZmJiMmIxZmYtNjc1ZC00MDZjLWJlNGItYjJkODIyYmI5MDQzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY3MzYxMTJhNzlkZmM2YzRkY2FjMDZkZSIsIm5iZiI6MTczMTU5Njg2MSwiY3NyZiI6ImYxMjM0NmU4LTYzMWYtNDZkZS1hYTZiLWE4N2U3OWFkNmRjZiIsImV4cCI6MTczMTYwMDQ2MX0.Gb5LkM_2_5RewOGVin5Jl7RPsHelPtl_JztQOlVGOBU
<br>

    returns:

    {
    "message": "Logged out successfully"
    }
<br>

## http://localhost:5000/api/profile/create_profile

    header:

    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTU5Njg2MSwianRpIjoiZmJiMmIxZmYtNjc1ZC00MDZjLWJlNGItYjJkODIyYmI5MDQzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY3MzYxMTJhNzlkZmM2YzRkY2FjMDZkZSIsIm5iZiI6MTczMTU5Njg2MSwiY3NyZiI6ImYxMjM0NmU4LTYzMWYtNDZkZS1hYTZiLWE4N2U3OWFkNmRjZiIsImV4cCI6MTczMTYwMDQ2MX0.Gb5LkM_2_5RewOGVin5Jl7RPsHelPtl_JztQOlVGOBU

    body:
        {
        "gender": "male",
        "sexual_preferences": "women", 
        "biography": "This is my user biography.",
        "interests": ["#reading", "#travel", "#photography"],
        "location": {
            "type": "Point",
            "coordinates": [-122.420679, 37.77493]
        }
    }

fills the profile with mandatory data
<br>


photos

tags