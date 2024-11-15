# app/routes/profile_view_endpoints.py

profile_view_bp = Blueprint('profile_view', __name__)

@profile_view_bp.route('/profile/<user_id>/view', methods=['POST'])
def record_profile_view(user_id):
    """Record when someone views a profile"""
    try:
        viewer_id = "current_user_id"  # Esto vendría del token de autenticación
        
        # No registrar si el usuario ve su propio perfil
        if viewer_id == user_id:
            return jsonify({
                "message": "Self profile view not recorded"
            }), 200
            
        ProfileViewModel.record_view(viewer_id, user_id)
        
        return jsonify({
            "message": "Profile view recorded successfully"
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@profile_view_bp.route('/profile/viewers', methods=['GET'])
def get_profile_viewers():
    """Get list of users who viewed current user's profile"""
    try:
        user_id = "current_user_id"  # Esto vendría del token de autenticación
        limit = request.args.get('limit', 10, type=int)
        
        viewers = ProfileViewModel.get_profile_viewers(user_id, limit)
        
        return jsonify({
            "viewers": viewers
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@profile_view_bp.route('/profile/views/stats', methods=['GET'])
def get_view_stats():
    """Get view statistics for current user's profile"""
    try:
        user_id = "current_user_id"  # Esto vendría del token de autenticación
        
        stats = ProfileViewModel.get_view_stats(user_id)
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500