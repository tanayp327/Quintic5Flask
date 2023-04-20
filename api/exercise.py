import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
import uuid

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
            eo = {'id': str(uuid.uuid4()), 'type': type, 'duration': duration, 'reps': reps, 'calories_burned': calories_burned}
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

    class _Update(Resource):
        def put(self, exercise_id):
            # read existing data from file
            with open(ExerciseAPI.filetype, 'r') as f:
                data = json.load(f)
            
            # find the exercise with the given id
            for i, exercise in enumerate(data):
                if 'id' in exercise and exercise['id'] == exercise_id:
                    # update the exercise with the new data
                    body = request.get_json()
                    if 'type' in body and len(body['type']) >= 2:
                        exercise['type'] = body['type']
                    if 'duration' in body and isinstance(body['duration'], int) and body['duration'] >= 1:
                        exercise['duration'] = body['duration']
                    if 'date' in body:
                        try:
                            datetime.strptime(body['date'], '%Y-%m-%d')
                            exercise['date'] = body['date']
                        except:
                            with open(ExerciseAPI.filetype, 'w') as f:
                                json.dump(data, f)
                            
                            return exercise, 200
                         # if no exercise with the given id was found, return error message
                        return {'message': f'Exercise with id {exercise_id} not found'}, 404

    class _Delete(Resource):
        def delete(self, exercise_id):
            # read existing data from file
            with open(ExerciseAPI.filetype, 'r') as f:
                data = json.load(f)
            
            # find the exercise with the given id
            for i, exercise in enumerate(data):
                if 'id' in exercise and exercise['id'] == exercise_id:
                    # remove the exercise from the list
                    del data[i]
                    # write updated data to file
                    with open(ExerciseAPI.filetype, 'w') as f:
                        json.dump(data, f)
                    # return success message
                    return {'message': f'Exercise with id {exercise_id} has been deleted'}
            
            # if no exercise with the given id was found, return error message
            return {'message': f'Exercise with id {exercise_id} not found'}, 404


    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Delete, '/delete/<int:exercise_id>')
    api.add_resource(_Read, '/')
    api.add_resource(_Update, '/exercise/<string:exercise_id>')