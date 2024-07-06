from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

WEATHER_ENDPOINT = "http://api.weatherapi.com/v1/current.json"

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Visitor')
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    try:
        location_response = requests.get(f'http://ip-api.com/json/154.161.179.228')
        location_data = location_response.json()
        city = location_data.get('city', 'Unknown location')

        weather_response = requests.get(WEATHER_ENDPOINT, params={'key': API_KEY, 'q': city})
        weather_data = weather_response.json()
        temperature = weather_data['current']['temp_c']

        return jsonify({
            'client_ip': client_ip,
            'location': city,
            'greeting': f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
