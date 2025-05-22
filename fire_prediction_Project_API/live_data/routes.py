#live_data/routes.py
from flask import Blueprint, request, jsonify
from joblib import load
import requests
live_data_bp= Blueprint('live_data', __name__)
 

api_key = 'bcefad9a65f2489fb2f231456252205'

@live_data_bp.route("/live_wind_data", methods=['POST'])
def live_wind_data():

    location = request.get_json()
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=no'
     # Call the external API
    response = requests.get(url)


    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from OpenWeatherMap"}), 500
    else:

        data = response.json()
        current = data.get('current',{})
        location = data.get('location', {})

           
        wind_info = {
            "wind_speed_kph": current.get('wind_kph'),
            "wind_speed_mph": current.get('wind_mph'),
            "wind_degree": current.get('wind_degree'),
            "wind_direction": current.get('wind_dir'),
            "gust_kph": current.get('gust_kph'),
            "gust_mph": current.get('gust_mph')
        }
        
        extra_info = {
            "temperature_c": current.get('temp_c'),
            "temperature_f": current.get('temp_f'),
            "humidity": current.get('humidity'),
            "feelslike_c": current.get('feelslike_c'),
            "feelslike_f": current.get('feelslike_f'),
            "condition_text": current.get('condition', {}).get('text'),
            "location_name": location.get('name'),
            "region": location.get('region'),
            "country": location.get('country'),
            "localtime": location.get('localtime')
        }

        result = {
            "wind": wind_info,
            "weather": extra_info
        }
        
        return jsonify(result)


