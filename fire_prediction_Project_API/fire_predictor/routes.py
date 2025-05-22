# fire_predictor/routes.py
from flask import Blueprint, request, jsonify
from joblib import load
fire_predictor_bp = Blueprint('fire_predictor', __name__)

regressor = load(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\fire_prediction_Project_API\Models\fire_predictor_regression_model.joblib')
classifier = load(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\fire_prediction_Project_API\Models\fire_predictor_classifier_model.joblib')

@fire_predictor_bp.route("/fire_predictor_regressor", methods=['POST'])
def fire_predictor_regressor():
    sample = request.get_json()
    prediction = regressor.predict(sample)
    return jsonify(prediction=prediction.tolist())

@fire_predictor_bp.route("/fire_predictor_classifier", methods=['POST'])
def fire_predictor_classifier():
    sample = request.get_json()
    prediction = classifier.predict(sample)
    return jsonify(prediction=prediction.tolist())