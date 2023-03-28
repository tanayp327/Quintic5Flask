import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

exercise_api = Blueprint('exercise_api', __name__, 
                         url_prefix='/api/exercises')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(exercise_api)

class ExerciseAPI:
    filetype = 'exercise_logs.json'

    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()

            ''' Avoid garbage in, error checking '''
            # validate type
            type = body.get('type')
            if type is None or len(type) < 2:
                return {'message': f'type is missing, or is less than 2 characters'}, 400
            # validate duration
            duration = body.get('duration')
            if duration is None or not isinstance(duration, int) or duration < 1:
                return {'message': f'Duration is missing, or is not a positive integer'}, 400
            # validate date
            date = body.get('date')
            if date is not None:
                try:
                    datetime.strptime(date, '%Y-%m-%d')
                except ValueError:
                    return {'message': f'Date is not in the correct format (YYYY-MM-DD)'}, 400

            # validate reps
            reps = body.get('reps')
            if reps is None or not isinstance(reps, int) or reps < 1:
                return {'message': f'Reps is missing, or is not a positive integer'}, 400

            # validate calories burned
            calories_burned = body.get('calories_burned')
            if calories_burned is None or not isinstance(calories_burned, int) or calories_burned < 1:
                return {'message': f'Calories burned is missing, or is not a positive integer'}, 400

            ''' #1: Key code block, setup EXERCISE OBJECT '''
            eo = {'type': type, 'duration': duration, 'reps': reps, 'calories_burned': calories_burned}
            if date is not None:
                eo['date'] = date

            ''' #2: Key Code block to add exercise to database '''
            # read existing data from file
            with open(ExerciseAPI.filetype, 'r') as f:
                data = json.load(f)
            # add new exercise to data
            data.append(eo)
            # write updated data to file
            with open(ExerciseAPI.filetype, 'w') as f:
                json.dump(data, f)

            # success returns json of exercise
            return jsonify(eo)

    class _Read(Resource):
        def get(self):
            # read existing data from file
            with open(ExerciseAPI.filetype, 'r') as f:
                data = json.load(f)
            # prepare output in json
            return jsonify(data)

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')