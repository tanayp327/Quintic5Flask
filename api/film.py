from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.films import Films

film_api = Blueprint('film_api', __name__,
                   url_prefix='/api/films')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(film_api)

class FilmAPI:    
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get("name")
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate uid            #if cid is None or len(cid) < 2:
             #   return {'message': f'User ID is missing, or is less than 2 characters'}, 210
            # look for password and dob
            #password = body.get('password')
            #dob = body.get('dob')
            year = int(body.get("year"))
            if year is None or year < 1800:
                return {'message': f'Year is missing, or is before 1800'}, 210
            ''' #1: Key code block, setup USER OBJECT '''
            epcount = int(body.get("epcount"))
            if epcount is None or epcount < 1:
                return {'message': f'Episode count is missing, or is not a valid count'}, 210
            eplist = body.get("eplist").split(',')
            if eplist is None or len(eplist) < 1:
                return {'message': f'Eplist is missing, or is less than 1 element'}, 210
            language = body.get("language")
            if language is None or len(language) < 1:
                return {'message': f'Language is missing, or is less than 1 character'}, 210
            trailer = body.get("trailer")
            fo = Films(name,year,epcount,language,trailer,eplist)
            
            ''' Additional garbage error checking '''
            # set password if provided
            #if password is not None:
             #   uo.set_password(password)
            # convert to date type
            #if dob is not None:
             #   try:
              #      uo.dob = datetime.strptime(dob, '%m-%d-%Y').date()
               # except:
                # return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 210
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            film = fo.create()
            # success returns json of user
            if film:
                return jsonify([film.read()])
            # failure returns error
            return {'message': f'Processed {film}, either a format error or Name {film} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            films = Films.query.all()    # read/extract all users from database
            json_ready = [film.read() for film in films]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    
    class _Update(Resource):
        def put(self):
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            
            name = body.get("name")
            # retrieve the object to be updated using a query


            film = Films.query.get(name)
            if film is None:
                return {'message': f'Name not in list'}, 210
               #d/ reaextract all users from database
            watched = body.get("watched")
            episodes = body.get("eps")
            film.update(watched,episodes)

            
            
    class _Delete(Resource):
        def delete(self,name):
            films1 = Films.query.all()
            if name == '-':
                films1 = Films.query.all()
                json_ready = [film.delete() for film in films1]
                return jsonify(json_ready)
            else:
                newfilm = Films.query.get(name)    # read/extract all users from database
                #print(newfilm)
                if newfilm:
                    newfilm.delete()
                    return {'message': f'successfully deleted {name}'}
                else:
                    return {'message': f'Film with name {name} not in list'}
            

        
            
    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Update, '/update')
    api.add_resource(_Delete, '/delete/<string:name>')