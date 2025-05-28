#live_data/routes.py
from flask import Blueprint, request, jsonify
from flask import abort
from datetime import datetime
import csv
import json
from joblib import load
import requests
import pandas as pd
import io

live_data_bp= Blueprint('live_data', __name__)
 

api_key = 'bcefad9a65f2489fb2f231456252205'


# Helper Functions


def live_data_helper(api_key,location):

    location = request.get_json()
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=no'
     # Call the external API
    response = requests.get(url)


    
    if response.status_code != 200:
        return {"error": "Failed to fetch data from OpenWeatherMap"}
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
        
        return result




def live_modis_data_helper(coordinates,date,date_range):

    #west,south,east,northwest,south,east,north
    #coordinates = "-125,24,-66,49"
    #date = '1/2025-05-23'
    #url = f'https://firms.modaps.eosdis.nasa.gov/api/area/csv/e3994c1efe51efb62bb18c25370bc03a/MODIS_NRT/{coordinates}/{date_range}/{date}'
    url = f'https://firms.modaps.eosdis.nasa.gov/api/area/csv/e3994c1efe51efb62bb18c25370bc03a/MODIS_NRT/{coordinates}/{date_range}/{date}'
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
        'frp': data['frp'],
        'daynight': data['daynight']               
    }
    



    

    
 
    
    
    
    
    return live_modis_data


#LIVE ROUTE FUNCTIONS

def live_location_data(location):

  
    

    # Extract necessary fields
  
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=no'

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from OpenWeatherMap"}), 500
    else:

        data = response.json()

        data = data.get("location", {})

        coordinate_date = {
            "longitude": data.get("lon"),
            "latitude": data.get("lat")
        }
      

           
       
    
    
        return coordinate_date

@live_data_bp.route("/live_wind_data", methods=['POST'])
def live_data():

    location = request.get_json()
    
    data = live_data_helper(api_key,location)


    
    return jsonify(data)


@live_data_bp.route("/live_Modis_data", methods=['POST'])
def live_modis_data(coordinates,date,date_range):

    #west,south,east,northwest,south,east,north

    
  

    #coordinates = "-125,24,-66,49"
    #date = '1/2025-05-23'

    json_data = request.get_json()



    data = live_modis_data_helper(coordinates,date,date_range)



    
    return jsonify(data)


#@live_data_bp.route("/live_combined_data", methods=['POST'])
def live_combined_data(location,date,date_range):
    #json_data = request.get_json()

    # Ensure JSON was sent
    #if not json_data:
        #return jsonify({"error": "Request body must be JSON"}), 400

    # Extract and validate required fields
    

    missing_fields = []
    if not location: missing_fields.append("location")
    if not date: missing_fields.append("date")
    if not date_range: missing_fields.append("date_range")

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Optional: Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

   
    coordinate_data = live_location_data(location)
    if isinstance(coordinate_data, tuple):  # Error returned from helper
        return coordinate_data

    lat = coordinate_data.get("latitude")
    lon = coordinate_data.get("longitude")

    if lat is None or lon is None:
        return jsonify({"error": "Unable to determine coordinates for the given location."}), 500

   
    south = lat - 1
    north = lat + 1
    west = lon - 1
    east = lon + 1
    coordinates = f"{west},{south},{east},{north}"

   
    wind_data = live_data_helper(api_key, location)
    if isinstance(wind_data, tuple):  # Check if error was returned
        return wind_data

 
    try:
        modis_data = live_modis_data_helper(coordinates, date, date_range)
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve MODIS data: {str(e)}"}), 500

    
    combined_data = {
        "weather": wind_data,
        "fireData": modis_data,
        "coordinates": coordinate_data
    }

    return combined_data



#FUTURE DATA ROUTE FUNCTIONS

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
