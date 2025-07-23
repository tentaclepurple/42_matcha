


# ENDPOINTS

## POST http://localhost:5000/api/users/register

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

## POST http://localhost:5000/api/users/login

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

 ## POST http://localhost:5000/api/users/logout
    
    header:

    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTU5Njg2MSwianRpIjoiZmJiMmIxZmYtNjc1ZC00MDZjLWJlNGItYjJkODIyYmI5MDQzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY3MzYxMTJhNzlkZmM2YzRkY2FjMDZkZSIsIm5iZiI6MTczMTU5Njg2MSwiY3NyZiI6ImYxMjM0NmU4LTYzMWYtNDZkZS1hYTZiLWE4N2U3OWFkNmRjZiIsImV4cCI6MTczMTYwMDQ2MX0.Gb5LkM_2_5RewOGVin5Jl7RPsHelPtl_JztQOlVGOBU
<br>

    returns:

    {
    "message": "Logged out successfully"
    }
<br>

## POST http://localhost:5000/api/profile/update_profile
Expects gender, sexual preferences, biography and interests as mandatory.
Create or update profile.

    header:


    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTU5Njg2MSwianRpIjoiZmJiMmIxZmYtNjc1ZC00MDZjLWJlNGItYjJkODIyYmI5MDQzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY3MzYxMTJhNzlkZmM2YzRkY2FjMDZkZSIsIm5iZiI6MTczMTU5Njg2MSwiY3NyZiI6ImYxMjM0NmU4LTYzMWYtNDZkZS1hYTZiLWE4N2U3OWFkNmRjZiIsImV4cCI6MTczMTYwMDQ2MX0.Gb5LkM_2_5RewOGVin5Jl7RPsHelPtl_JztQOlVGOBU
<br>
    body:
        {
        "gender": "male",
        "sexual_preferences": "women", 
        "biography": "This is my user biography.",
        "interests": ["reading", "travel", "photography"],
        "location": {
            "type": "Point",
            "coordinates": [-122.420679, 37.77493]
        }
    }

fills the profile with mandatory data
<br>

## PUT http://localhost:5000/api/profile/update_photo/<int>

Upload a file with size and extension restrictions with its index

    header:

    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTU5Njg2MSwianRpIjoiZmJiMmIxZmYtNjc1ZC00MDZjLWJlNGItYjJkODIyYmI5MDQzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY3MzYxMTJhNzlkZmM2YzRkY2FjMDZkZSIsIm5iZiI6MTczMTU5Njg2MSwiY3NyZiI6ImYxMjM0NmU4LTYzMWYtNDZkZS1hYTZiLWE4N2U3OWFkNmRjZiIsImV4cCI6MTczMTYwMDQ2MX0.Gb5LkM_2_5RewOGVin5Jl7RPsHelPtl_JztQOlVGOBU

<br>

    body:

    form-data
    photo: <file>

<br>

## PUT http://localhost:5000/api/profile/update_avatar/<int>

Select the profile photo/avatar from the existing 5 images

    header:

    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTU5Njg2MSwianRpIjoiZmJiMmIxZmYtNjc1ZC00MDZjLWJlNGItYjJkODIyYmI5MDQzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY3MzYxMTJhNzlkZmM2YzRkY2FjMDZkZSIsIm5iZiI6MTczMTU5Njg2MSwiY3NyZiI6ImYxMjM0NmU4LTYzMWYtNDZkZS1hYTZiLWE4N2U3OWFkNmRjZiIsImV4cCI6MTczMTYwMDQ2MX0.Gb5LkM_2_5RewOGVin5Jl7RPsHelPtl_JztQOlVGOBU

<br>

## GET http://localhost:5000/api/tags/search?q=p

Search tags by match. For autocomplete in front 
q=<pattern>

    header:

    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTU5Njg2MSwianRpIjoiZmJiMmIxZmYtNjc1ZC00MDZjLWJlNGItYjJkODIyYmI5MDQzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY3MzYxMTJhNzlkZmM2YzRkY2FjMDZkZSIsIm5iZiI6MTczMTU5Njg2MSwiY3NyZiI6ImYxMjM0NmU4LTYzMWYtNDZkZS1hYTZiLWE4N2U3OWFkNmRjZiIsImV4cCI6MTczMTYwMDQ2MX0.Gb5LkM_2_5RewOGVin5Jl7RPsHelPtl_JztQOlVGOBU

<br>

    returns:

    {
    "tags": [
        "patchwork",
        "pesca",
        "photography"
    ]
}

<br>

## GET http://localhost:5000/api/tags/popular?limit=4
limit=<number of results>
also works without filter

    header:

    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTU5Njg2MSwianRpIjoiZmJiMmIxZmYtNjc1ZC00MDZjLWJlNGItYjJkODIyYmI5MDQzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY3MzYxMTJhNzlkZmM2YzRkY2FjMDZkZSIsIm5iZiI6MTczMTU5Njg2MSwiY3NyZiI6ImYxMjM0NmU4LTYzMWYtNDZkZS1hYTZiLWE4N2U3OWFkNmRjZiIsImV4cCI6MTczMTYwMDQ2MX0.Gb5LkM_2_5RewOGVin5Jl7RPsHelPtl_JztQOlVGOBU
<br>
    returns:
        {
        "tags": [
            {
                "count": 16,
                "name": "caza"
            },
            {
                "count": 16,
                "name": "literature"
            },
            {
                "count": 6,
                "name": "patchwork"
            },
            {
                "count": 3,
                "name": "cooking"
            }
        ]
    }


## GET http://localhost:5000/api/tags/user_common?limit=2
    Returns users with tags in common

    header:

        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTU5Njg2MSwianRpIjoiZmJiMmIxZmYtNjc1ZC00MDZjLWJlNGItYjJkODIyYmI5MDQzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY3MzYxMTJhNzlkZmM2YzRkY2FjMDZkZSIsIm5iZiI6MTczMTU5Njg2MSwiY3NyZiI6ImYxMjM0NmU4LTYzMWYtNDZkZS1hYTZiLWE4N2U3OWFkNmRjZiIsImV4cCI6MTczMTYwMDQ2MX0.Gb5LkM_2_5RewOGVin5Jl7RPsHelPtl_JztQOlVGOBU
<br>
    returns:

    {
        "users": [
            {
                "common_tags": [
                    "caza",
                    "flamenco"
                ],
                "common_tags_count": 3,
                "user_id": "67373d56d523c57ea25c5848",
                "username": "farina"
            }
        ]
    }
