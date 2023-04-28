from flask import Flask, jsonify
import requests
import pandas as pd

app = Flask(__name__)

@app.route('/cities/<city>')
def get_city_weather(city):
    url = f"https://community-open-weather-map.p.rapidapi.com/weather?q={city}&units=metric"
    headers = {
        'x-rapidapi-key': 'b1182b6a64mshff6fcbeabf69dc2p199d99jsn12adc869f7a0',
        'x-rapidapi-host': 'community-open-weather-map.p.rapidapi.com'
    }
    response = requests.request("GET", url, headers=headers).json()
    
    # Create a pandas DataFrame with the relevant data
    data = {
        'city': [response['name']],
        'country': [response['sys']['country']],
        'temperature': [response['main']['temp']],
        'humidity': [response['main']['humidity']],
        'wind_speed': [response['wind']['speed']],
        'description': [response['weather'][0]['description']]
    }
    df = pd.DataFrame(data)
    
    # Return the DataFrame as a JSON response
    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
