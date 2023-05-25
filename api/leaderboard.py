from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import db
from model.leaderboard import LeaderboardEntry

leaderboard_api = Blueprint('leaderboard_api', __name__, url_prefix='/api/leaderboard')
api = Api(leaderboard_api)

class LeaderboardAPI(Resource):
    class Create(Resource):
        def post(self):
            try:
                data = request.get_json()
                rank = data.get('rank')
                name = data.get('name')
                score = data.get('score')

                new_entry = LeaderboardEntry(rank=rank, name=name, score=score)
                created_entry = new_entry.create()

                if created_entry:
                    return jsonify(created_entry.read())
                else:
                    return {'message': 'Error creating leaderboard entry.'}, 500
            except Exception as e:
                return {'message': str(e)}, 500

    class Read(Resource):
        def get(self):
            entries = LeaderboardEntry.query.all()
            leaderboard = [entry.read() for entry in entries]
            return jsonify(leaderboard)

    class Update(Resource):
        def put(self, entry_id):
            try:
                entry = LeaderboardEntry.query.get(entry_id)
                if not entry:
                    return {'message': 'Leaderboard entry not found.'}, 404

                data = request.get_json()
                rank = data.get('rank')
                name = data.get('name')
                score = data.get('score')

                entry.update(rank=rank, name=name, score=score)
                return jsonify(entry.read())
            except Exception as e:
                return {'message': str(e)}, 500

    class Delete(Resource):
        def delete(self, entry_id):
            try:
                entry = LeaderboardEntry.query.get(entry_id)
                if not entry:
                    return {'message': 'Leaderboard entry not found.'}, 404

                entry.delete()
                return {'message': 'Leaderboard entry deleted successfully.'}
            except Exception as e:
                return {'message': str(e)}, 500

    api.add_resource(Create, "/")
    api.add_resource(Read, "/")
    api.add_resource(Update, "/<int:entry_id>")
    api.add_resource(Delete, "/<int:entry_id>")

