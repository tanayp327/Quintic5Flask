from flask import Flask, jsonify, request, Blueprint, app
from flask_restful import Resource, Api

rocket_api = Blueprint('rocket_api', __name__, 
                            url_prefix='/api/rocket')
api = Api(rocket_api)

# Constants
GRAVITY = 9.8  # Acceleration due to gravity

# Create a resource for handling game requests
class GameResource(Resource):
    def post(self):
        # Get the player's input from the request
        data = request.get_json()

        # Process the player's input and calculate the rocket's trajectory
        thrust = data['thrust']
        drag = data['drag']
        time = data['time']

        velocity = thrust - drag - GRAVITY * time
        altitude = 0.5 * (thrust - drag) * time**2 - GRAVITY * time**2

        # Return the result as a JSON response
        return jsonify(velocity=velocity, altitude=altitude)

# Add the resource to the API
api.add_resource(GameResource, '/game')
