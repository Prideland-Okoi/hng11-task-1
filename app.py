from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)


@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    weather_api_key = os.getenv('WEATHER_API_KEY')

    try:
        # Get location data using IP
        # location_response = requests.get(f'https://ipapi.co/{client_ip}/json/')
        location_response = requests.get(f'https://ipinfo.io/{client_ip}/json')
        # location_response = requests.get('https://freegeoip.app/json/')
        location_data = location_response.json()
        location = location_data.get('city', 'Unknown Location')

        # Log location data for debugging
        print(f"Location data: {location_data}")

        # Get weather data using location
        weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric')
        weather_data = weather_response.json()

        # Log weather data for debugging
        print(f"Weather data: {weather_data}")

        # Check if 'main' key exists in the weather response
        if 'main' not in weather_data:
            raise KeyError(
                f"Key 'main' not found in weather data: {weather_data}")

        temperature = weather_data['main']['temp']

        return jsonify({
            "client_ip": client_ip,
            "location": location,
            "greeting": f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {location}"
        })
    except Exception as e:
        # Log the error for debugging
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
