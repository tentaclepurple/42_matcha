# app/routes/tags.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import UserModel
from ..config.database import mongo
from bson import ObjectId


tags_bp = Blueprint('tags', __name__)

# Search with autocomplete
@tags_bp.route('/search', methods=['GET'])
@jwt_required()
def search_tags():
   try:
       query = request.args.get('q', '').lower()
       if not query:
           return jsonify({'tags': []}), 200

       tags = mongo.db.tags.find({
           'name': {'$regex': f'^{query}'}
       }).limit(10)

       return jsonify({
           'tags': [tag['name'] for tag in tags]
       }), 200

   except Exception as e:
       return jsonify({'error': str(e)}), 500


@tags_bp.route('/popular', methods=['GET'])
@jwt_required()
def get_popular_tags():
   try:
       limit = int(request.args.get('limit', 20))
       
       tags = mongo.db.tags.find().sort('count', -1).limit(limit)
       
       return jsonify({
           'tags': [{
               'name': tag['name'],
               'count': tag['count']
           } for tag in tags]
       }), 200

   except Exception as e:
       return jsonify({'error': str(e)}), 500


@tags_bp.route('/user_common', methods=['GET'])
@jwt_required()
def find_users_by_common_tags():
   try:
       current_user_id = get_jwt_identity()
       current_user = UserModel.find_by_id(current_user_id)
       user_tags = current_user.get('interests', [])
       limit = int(request.args.get('limit', len(user_tags)))  # Si no se especifica, usa todos

       pipeline = [
           {
               '$match': {
                   '_id': {'$ne': ObjectId(current_user_id)},
                   'interests': {'$in': user_tags}
               }
           },
           {
               '$project': {
                   'username': 1,
                   'interests': 1,
                   'common_tags': {
                       '$slice': [  # Limitar número de tags comunes
                           {'$setIntersection': ['$interests', user_tags]},
                           limit
                       ]
                   },
                   'common_tags_count': {
                       '$size': {
                           '$setIntersection': ['$interests', user_tags]
                       }
                   }
               }
           },
           {'$sort': {'common_tags_count': -1}},
           {'$limit': 20}
       ]

       users = list(mongo.db.users.aggregate(pipeline))

       return jsonify({
           'users': [{
               'user_id': str(user['_id']),
               'username': user['username'],
               'common_tags_count': user['common_tags_count'],
               'common_tags': user['common_tags']
           } for user in users]
       }), 200

   except Exception as e:
       return jsonify({'error': str(e)}), 500