# app/routes/like_endpoints.py

like_bp = Blueprint('like', __name__)


@like_bp.route('/profile/<user_id>/<action>', methods=['POST'])
def add_like(user_id, action):
    """Add a like or unlike to a profile"""
    if action not in ["like", "unlike"]:
        return jsonify({
            "error": "Invalid action. Must be 'like' or 'unlike'"
        }), 400

    try:
        from_user_id = "current_user_id"  # Esto vendría del token de autenticación
        
        LikeModel.add_like(from_user_id, user_id, action)
        
        response = {
            "message": f"Successfully added {action}",
            "is_match": False
        }
        
        if action == "like":
            # Verificar si hay match
            is_match = LikeModel.check_is_match(from_user_id, user_id)
            if is_match:
                response.update({
                    "message": "It's a match!",
                    "is_match": True
                })
        
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@like_bp.route('/received', methods=['GET'])
def get_received_likes():
    """Get likes/unlikes received by the current user"""
    try:
        user_id = "current_user_id"  # Esto vendría del token de autenticación
        like_type = request.args.get('type')  # 'like', 'unlike' o None para todos
        likes = LikeModel.get_likes_received(user_id, like_type)
        
        return jsonify({
            "likes": likes
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500