#live_data/routes.py
from flask import Blueprint, request, jsonify
import csv
import json
from joblib import load
import requests
import pandas as pd
import io

live_data_bp= Blueprint('live_data', __name__)
 

api_key = 'bcefad9a65f2489fb2f231456252205'

@live_data_bp.route("/live_data", methods=['POST'])
def live_data():

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
        
      

        result = {
            "wind": wind_info,
            
        }
        
        return jsonify(result)


@live_data_bp.route("/future_data", methods=['POST'])
def future_data():

    location = "Riverside"
    url = f'http://api.weatherapi.com/v1/future.json?key={api_key}&q={location}&dt=2025-06-22'
     # Call the external API
    response = requests.get(url)

    data = response.json()

  

    locationData = data.get('location',{})

    geolocationData = {
        "lat": locationData.get('lat'),
        "long": locationData.get('lon')
    }

    windData = data.get('forecast')
    windData =  windData.get('forecastday')
    windData = windData[0]
    windData = windData.get('day')

    windData = {
        'wind_sample' : windData.get('maxwind_mph') * 0.868976  #mph -> knots
    }
 
    
    result = {
        "wind": windData,
        "location": geolocationData
    }

    
    
    return jsonify(result)


@live_data_bp.route("/live_Modis_data", methods=['POST'])
def live_modis_data():

    #west,south,east,northwest,south,east,north
    coordinates = "-125,24,-66,49"
    date = '1/2025-05-23'
    url = f'https://firms.modaps.eosdis.nasa.gov//api/area/csv/e3994c1efe51efb62bb18c25370bc03a/MODIS_NRT/{coordinates}/{date}'
    
    response = requests.get(url)

    data = response.text


    csv_file = io.StringIO(response.text)

    dataset = pd.read_csv(csv_file)

    random_row = dataset.sample(n=1).iloc[0]
   
    data = random_row
    #brightness	scan	track	bright_t31	frp
    live_modis_data = {
    'brightness': data['brightness'],     
    'scan': data['scan'],                
    'track': data['track'],               
    'bright_t31': data['bright_t31'],    
    'frp': data['frp']                    
    }
    

    print(live_modis_data)

  





    
    return live_modis_data