# app/routes/match_endpoints.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..config.database import mongo
from ..models.user import UserModel
from bson import ObjectId


match_bp = Blueprint('match', __name__)


@match_bp.route('/suggestions', methods=['GET'])
@jwt_required()
def get_suggestions():
    try:
        current_user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404

        # Get filtering and sorting parameters
        min_age = request.args.get('min_age', type=int)
        max_age = request.args.get('max_age', type=int)
        min_fame = request.args.get('min_fame', type=float)
        max_fame = request.args.get('max_fame', type=float)
        max_distance = request.args.get('max_distance', type=float)  # in km
        min_common_tags = request.args.get('min_common_tags', type=int)
        sort_by = request.args.get('sort_by', 'distance')  # distance, age, fame_rating, common_tags
        sort_order = request.args.get('sort_order', 'asc')  

        # Get user gender preferences
        user_gender = current_user.get('gender')
        user_preferences = current_user.get('sexual_preferences')

        # Build gender query
        gender_query = {
            '$or': [
                # If bisexual, accepts male and female
                {
                    'sexual_preferences': 'bisexual',
                    'gender': {'$in': ['male', 'female']}
                },
                # Or if has preference for my specific gender
                {'sexual_preferences': user_gender},
                # Or if has 'other' preference and I'm 'other'
                {
                    'sexual_preferences': 'other',
                    'gender': 'other'
                }
            ]
        }

        # Adjust based on current user preferences
        if user_preferences == 'male':
            gender_query['gender'] = 'male'
        elif user_preferences == 'female':
            gender_query['gender'] = 'female'
        elif user_preferences == 'other':
            gender_query['gender'] = 'other'
        elif user_preferences == 'bisexual':
            gender_query['gender'] = {'$in': ['male', 'female']}
        else:  # If None, consider as bisexual
            gender_query['gender'] = {'$in': ['male', 'female']}

        # Pipeline with $geoNear first
        pipeline = [
            {
                '$geoNear': {
                    'near': current_user.get('location', {'type': 'Point', 'coordinates': [0, 0]}),
                    'distanceField': 'distance',
                    'spherical': True,
                    'query': {
                        '$and': [
                            # Exclude users who have blocked current user
                            {'blocked_users': {'$ne': ObjectId(current_user_id)}},
                            # exclude blocked users too
                            {'_id': {'$nin': current_user.get('blocked_users', [])}},
                            # Only verified and completed profiles
                            {'verified': True},
                            {'profile_completed': True},
                            # Different user than current
                            {'_id': {'$ne': ObjectId(current_user_id)}},
                            # Apply gender filters
                            gender_query
                        ]
                    }
                }
            },
            # Calculate common tags
            {
                '$addFields': {
                    'common_tags': {
                        '$size': {
                            '$setIntersection': ['$interests', current_user.get('interests', [])]
                        }
                    }
                }
            }
        ]

        # Apply filters
        match_conditions = {}

        # Age filter
        if min_age is not None or max_age is not None:
            match_conditions['age'] = {}
            if min_age is not None:
                match_conditions['age']['$gte'] = min_age
            if max_age is not None:
                match_conditions['age']['$lte'] = max_age

        # Fame rating filters
        if min_fame is not None or max_fame is not None:
            match_conditions['fame_rating'] = {}
            if min_fame is not None:
                match_conditions['fame_rating']['$gte'] = min_fame
            if max_fame is not None:
                match_conditions['fame_rating']['$lte'] = max_fame

        # Distance filter
        if max_distance is not None:
            if max_distance == 0:
                match_conditions['distance'] = 0  # Exact same location
            else:
                match_conditions['distance'] = {'$lte': max_distance * 1000}  # Convert to meters

        # Other filters
        if min_common_tags:
            match_conditions['common_tags'] = {'$gte': min_common_tags}

        if match_conditions:
            pipeline.append({'$match': match_conditions})

        # Sorting
        sort_direction = 1 if sort_order == 'asc' else -1
        sort_field = {
            'distance': 'distance',
            'age': 'age',
            'fame_rating': 'fame_rating',
            'common_tags': 'common_tags'
        }.get(sort_by, 'distance')

        pipeline.append({'$sort': {sort_field: sort_direction}})

        # Get results
        matches = list(mongo.db.users.aggregate(pipeline))

        # Format response
        return jsonify({
            'current_user_info': {
                'gender': current_user.get('gender'),
                'sexual_preferences': current_user.get('sexual_preferences'),
                'interests': current_user.get('interests'),
                'location': current_user.get('location')
            },
            'filter_params': {
                'min_age': min_age,
                'max_age': max_age,
                'min_fame': min_fame,
                'max_fame': max_fame,
                'max_distance': max_distance,
                'min_common_tags': min_common_tags,
                'sort_by': sort_by,
                'sort_order': sort_order
            },
            'matches': [{
                'user_id': str(match['_id']),
                'username': match['username'],
                'gender': match.get('gender'),
                'sexual_preferences': match.get('sexual_preferences'),
                'age': match['age'],
                'distance': round(match['distance'] / 1000, 2),  # km
                'location': match.get('location'),
                'common_tags': match['common_tags'],
                'common_tags_list': list(set(match.get('interests', [])) & 
                                     set(current_user.get('interests', []))),
                'interests': match.get('interests', []),
                'fame_rating': match['fame_rating'],
                'profile_photo': next(
                    (photo['url'] for photo in match.get('photos', []) 
                     if photo.get('is_profile')), 
                    None
                )
            } for match in matches]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@match_bp.route('/search', methods=['GET'])
@jwt_required()
def advanced_search():
    try:
        current_user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404

        # Get all search parameters
        min_age = request.args.get('min_age', type=int)
        max_age = request.args.get('max_age', type=int)
        min_fame = request.args.get('min_fame', type=float)
        max_fame = request.args.get('max_fame', type=float)
        max_distance = request.args.get('max_distance', type=float)
        interests = request.args.getlist('interests')  # Can receive multiple tags
        gender = request.args.get('gender')  # male, female, other
        sexual_preference = request.args.get('sexual_preference')  # male, female, bisexual, other
        
        # Sorting parameters
        sort_by = request.args.get('sort_by', 'distance')  # distance, age, fame_rating
        sort_order = request.args.get('sort_order', 'asc')

        # Build pipeline
        pipeline = [
            {
                '$geoNear': {
                    'near': current_user.get('location', {'type': 'Point', 'coordinates': [0, 0]}),
                    'distanceField': 'distance',
                    'spherical': True,
                    'query': {
                        '$and': [
                            # Exclude users who have blocked current user
                            {'blocked_users': {'$ne': ObjectId(current_user_id)}},
                            # exclude blocked users too
                            {'_id': {'$nin': current_user.get('blocked_users', [])}},
                            # Only verified and completed profiles
                            {'verified': True},
                            {'profile_completed': True},
                            # Different user than current
                            {'_id': {'$ne': ObjectId(current_user_id)}}
                        ]
                    }
                }
            }
        ]

        # Build search conditions
        match_conditions = {}

        # Age filters
        if min_age is not None or max_age is not None:
            match_conditions['age'] = {}
            if min_age is not None:
                match_conditions['age']['$gte'] = min_age
            if max_age is not None:
                match_conditions['age']['$lte'] = max_age

        # Fame rating filters
        if min_fame is not None or max_fame is not None:
            match_conditions['fame_rating'] = {}
            if min_fame is not None:
                match_conditions['fame_rating']['$gte'] = min_fame
            if max_fame is not None:
                match_conditions['fame_rating']['$lte'] = max_fame

        # Gender and preferences filters
        if gender:
            match_conditions['gender'] = gender
        if sexual_preference:
            match_conditions['sexual_preferences'] = sexual_preference

        # Distance filter
        if max_distance:
            match_conditions['distance'] = {'$lte': max_distance * 1000}

        # Interests filter
        if interests:
            match_conditions['interests'] = {'$all': interests}

        # Add match conditions to pipeline
        if match_conditions:
            pipeline.append({'$match': match_conditions})

        # Sorting
        sort_direction = 1 if sort_order == 'asc' else -1
        sort_field = {
            'distance': 'distance',
            'age': 'age',
            'fame_rating': 'fame_rating'
        }.get(sort_by, 'distance')

        pipeline.append({
            '$sort': {
                sort_field: sort_direction,
                'username': 1
            }
        })

        # Get results
        results = list(mongo.db.users.aggregate(pipeline))

        # Format response
        return jsonify({
            'search_params': {
                'min_age': min_age,
                'max_age': max_age,
                'min_fame': min_fame,
                'max_fame': max_fame,
                'max_distance': max_distance,
                'interests': interests,
                'gender': gender,
                'sexual_preference': sexual_preference,
                'sort_by': sort_by,
                'sort_order': sort_order
            },
            'results': [{
                'user_id': str(result['_id']),
                'username': result['username'],
                'profile_photo': next(
                    (photo['url'] for photo in result.get('photos', []) 
                     if photo.get('is_profile')), 
                    None
                ),
                'age': result.get('age'),
                'gender': result.get('gender'),
                'location': result.get('location'),
                'sexual_preferences': result.get('sexual_preferences'),
                'distance': round(result['distance'] / 1000, 2),  # km
                'fame_rating': result.get('fame_rating'),
                'interests': result.get('interests', [])
            } for result in results]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
