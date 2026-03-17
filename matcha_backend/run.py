from app import create_app
from flask_cors import CORS

app = create_app()

cors_config = {
    "origins": "*", 
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": [
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Credentials"
    ],
    "supports_credentials": False,  # ← quitar si pones "*"
    "max_age": 3600
}

CORS(app, resources={
    r"/api/*": cors_config # applies to all API routes
})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
