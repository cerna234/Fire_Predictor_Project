
from flask import Flask, jsonify, request
from joblib import load



app = Flask(__name__)


regressor = load(r'/Users/miguelcerna/Desktop/Fire_Predictor_Project/fire_prediction_Project_API/Models/fire_predictor_regression_model.joblib')
classifier = load(r'/Users/miguelcerna/Desktop/Fire_Predictor_Project/fire_prediction_Project_API/Models/fire_predictor_classifier_model.joblib')

@app.route("/")
def home():
    
    return "up and Running"

@app.route("/fire_Predictor_regressor",methods=['GET', 'POST'])
def fire_predictor_regressor():

    
    sample = request.get_json()
    
    prediction = regressor.predict(sample)

    print(prediction)

    return jsonify(prediction=prediction.tolist())

@app.route("/fire_Predictor_Classifier",methods=['GET', 'POST'])
def fire_predictor_Classifier():
    
    
    sample = request.get_json()
    
    prediction = classifier.predict(sample)
    
    print(prediction)

    return jsonify(prediction=prediction.tolist())


if __name__ == '__main__':
    app.run(debug=True)