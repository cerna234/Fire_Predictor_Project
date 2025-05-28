# fire_predictor/routes.py
from flask import Blueprint, request, jsonify
from joblib import load
fire_predictor_bp = Blueprint('fire_predictor', __name__)
from live_data.routes import live_combined_data

regressor = load(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\fire_prediction_Project_API\Models\fire_predictor_regression_model.joblib')
classifier = load(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\fire_prediction_Project_API\Models\fire_predictor_classifier_model.joblib')


def extract_features(data):
    weather = data.get("weather", {}).get("wind", {})
    fire = data.get("fireData", {})
    coords = data.get("coordinates", {})

    features = [[
        float(coords.get("latitude", 0)), #lat
        float(coords.get("longitude", 0)), #lon
        float(fire.get("brightness", 0)), #brightness
        float(fire.get("scan", 0)), #scan
        float(fire.get("track",0)), #track
        float(fire.get("bright_t31", 0)), #bright_t31
        float(fire.get("frp", 0)), #frp
        fire.get("daynight"), #daynight
        0, #type
        19, #date_time(needs to be formatted in a date such as day 19, 18)
        171, #Sample Measurement
        "Degrees Compass",# Units of Measure: will be updating this to combine wind speed and direction
        1 #mdl
        
    ]]

    return features

@fire_predictor_bp.route("/fire_predictor_regressor", methods=['POST'])
def fire_predictor_regressor():
  
    json_data = request.get_json()
    #SAMPLE
    '''
        [
    [
        334.0961,
        -117.5279,
        301.4,
        1,
        1,
        289.6,
        3.3,
        "D",
        2,
        19,
        171,
        "Degrees Compass",
        1
    ]
    ]
    '''

    # Ensure JSON was sent
    if not json_data:
        return jsonify({"error": "Request body must be JSON"}), 400

   
    # Extract and validate required fields
    location = json_data.get("location")
    date = json_data.get("date")
    date_range = json_data.get("date_range")


   
    sampleData = extract_features(live_combined_data(location,date,date_range))
    print(sampleData)

    prediction = regressor.predict(sampleData)
    
    
    return jsonify(prediction=prediction.tolist())





@fire_predictor_bp.route("/fire_predictor_classifier", methods=['POST'])
def fire_predictor_classifier():
    sample = request.get_json()
    prediction = classifier.predict(sample)
    return jsonify(prediction=prediction.tolist())