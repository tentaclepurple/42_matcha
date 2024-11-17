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

       # Obtener parámetros de filtrado y ordenamiento
       min_age = request.args.get('min_age', type=int)
       max_age = request.args.get('max_age', type=int)
       min_fame = request.args.get('min_fame', type=float)
       max_fame = request.args.get('max_fame', type=float)
       max_distance = request.args.get('max_distance', type=float)  # en km
       min_common_tags = request.args.get('min_common_tags', type=int)
       sort_by = request.args.get('sort_by', 'distance')  # distance, age, fame_rating, common_tags
       sort_order = request.args.get('sort_order', 'asc')  # asc o desc
           
       # Determinar preferencias de género
       gender_filter = []
       if current_user.get('sexual_preferences') == 'male':
           gender_filter = ['male']
       elif current_user.get('sexual_preferences') == 'female':
           gender_filter = ['female']
       else:  # bisexual o no especificado
           gender_filter = ['male', 'female', 'other']

       # Pipeline con $geoNear primero
       pipeline = [
           {
               '$geoNear': {
                   'near': current_user.get('location', {'type': 'Point', 'coordinates': [0, 0]}),
                   'distanceField': 'distance',
                   'spherical': True,
                   'query': {  # Filtros básicos en query de $geoNear
                       '_id': {'$ne': ObjectId(current_user_id)},
                       'gender': {'$in': gender_filter},
                       '_id': {'$nin': current_user.get('blocked_users', [])}
                   }
               }
           },
           # Calcular tags en común
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

       # Aplicar filtros
       match_conditions = {}

       # Filtro de edad
       if min_age is not None or max_age is not None:
           match_conditions['age'] = {}
           if min_age is not None:
               match_conditions['age']['$gte'] = min_age
           if max_age is not None:
               match_conditions['age']['$lte'] = max_age

       # Filtros de fame rating
       if min_fame is not None or max_fame is not None:
           match_conditions['fame_rating'] = {}
           if min_fame is not None:
               match_conditions['fame_rating']['$gte'] = min_fame
           if max_fame is not None:
               match_conditions['fame_rating']['$lte'] = max_fame

       # Filtro de distancia
       if max_distance is not None:  # Si se especifica un max_distance
           if max_distance == 0:
               match_conditions['distance'] = 0  # Exactamente misma ubicación
           else:
               match_conditions['distance'] = {'$lte': max_distance * 1000}  # Convertir a metros

       # Otros filtros
       if min_common_tags:
           match_conditions['common_tags'] = {'$gte': min_common_tags}

       if match_conditions:
           pipeline.append({'$match': match_conditions})

       # Ordenamiento
       sort_direction = 1 if sort_order == 'asc' else -1
       sort_field = {
           'distance': 'distance',
           'age': 'age',
           'fame_rating': 'fame_rating',
           'common_tags': 'common_tags'
       }.get(sort_by, 'distance')

       pipeline.append({'$sort': {sort_field: sort_direction}})

       # Obtener resultados
       matches = list(mongo.db.users.aggregate(pipeline))

       # Formatear respuesta
       return jsonify({
           'current_user_info': {
               'gender': current_user.get('gender'),
               'sexual_preferences': current_user.get('sexual_preferences'),
               'interests': current_user.get('interests'),
               'location': current_user.get('location')
           },
           'filter_params': {
               'gender_filter': gender_filter,
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
               'fame_rating': match['fame_rating']
           } for match in matches]
       }), 200

   except Exception as e:
       return jsonify({'error': str(e)}), 500