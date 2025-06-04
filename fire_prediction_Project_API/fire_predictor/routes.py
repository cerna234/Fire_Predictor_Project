# fire_predictor/routes.py
from flask import Blueprint, request, jsonify
from joblib import load
fire_predictor_bp = Blueprint('fire_predictor', __name__)
from live_data.routes import live_combined_data

regressor = load(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\RegressionModel\model_20250604_111457.joblib')
classifier = load(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\classifierModel\model_20250603_162003.joblib')


def extract_features(data):
    if not data:
        return []

    coords = data.get("coordinates", {})
    weather = data.get("weather", {}).get("wind", {})
    fire = data.get("fireData", {})
    

    features = [[
        float(coords.get("latitude", 0)),
        float(coords.get("longitude", 0)),
        float(fire.get("brightness", 0)),
        float(fire.get("scan", 0)),
        float(fire.get("track", 0)),
        float(fire.get("bright_t31", 0)),
        float(fire.get("frp", 0)),
        fire.get("daynight", "D"),
        0, #type
        7, #Day of week
        0.1, #mdl
        weather.get("gust_mph") #wind measurement
    ]]


    return features

@fire_predictor_bp.route("/fire_predictor_regressor", methods=['POST'])
def fire_predictor_regressor():
  
    json_data = request.get_json()
    #SAMPLE
    
 

   
    # Ensure JSON was sent
    if not json_data:
        return jsonify({"error": "Request body must be JSON"}), 400

   
    # Extract and validate required fields
    location = json_data.get("location")
    date = json_data.get("date")
    date_range = json_data.get("date_range")
  
    response, status_code = live_combined_data(location, date, date_range)
    
   

  
    if status_code != 200:
        return response, status_code
    


  
    data = response.get_json()  

    sampleData = extract_features(data)
    
    bounding_Box = data.get("bounding_Box")
    prediction = regressor.predict(sampleData)
  
    
    outputData = {
        "Prediction": prediction.tolist(),
        "boundingBox": bounding_Box
       
    }
    
    
    return outputData







@fire_predictor_bp.route("/fire_predictor_classifier", methods=['POST'])
def fire_predictor_classifier():

    json_data = request.get_json()
    #SAMPLE
    
 

   
    # Ensure JSON was sent
    if not json_data:
        return jsonify({"error": "Request body must be JSON"}), 400

   
    # Extract and validate required fields
    location = json_data.get("location")
    date = json_data.get("date")
    date_range = json_data.get("date_range")
  
    response, status_code = live_combined_data(location, date, date_range)
    
   

  
    if status_code != 200:
        return response, status_code
    


  
    data = response.get_json()  
   
    sampleData = extract_features(data)
    

    prediction = classifier.predict(sampleData)
  
    
    
    return jsonify(prediction=prediction.tolist())

   