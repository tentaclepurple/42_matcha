from app import create_app
from flask_cors import CORS

app = create_app()

cors_config = {
    "origins": [
        "http://localhost:5173",  # development frontend
        "http://127.0.0.1:5173"   # common alias
    ],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # methods allowed
    "allow_headers": [
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Credentials"
    ],
    "supports_credentials": True,  # mandatory for cookies to be allowed
    "max_age": 3600  # time in seconds that preflight response should be cached
}

CORS(app, resources={
    r"/api/*": cors_config # applies to all API routes
})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
