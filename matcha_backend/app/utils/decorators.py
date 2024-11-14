# app/utils/decorators.py
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify

#unused
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except:
            return jsonify({"error": "Invalid or missing token"}), 401
    return decorated_function
