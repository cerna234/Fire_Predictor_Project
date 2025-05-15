
from flask import Flask, jsonify
from joblib import load



app = Flask(__name__)


regressor = load(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\RegressionModel\fire_predictor_pipeline.joblib')
classifier = load(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\classifierModel\fire_predictor_pipeline_Classifier.joblib')

@app.route("/")
def home():
    
    return "up and Running"

@app.route("/fire_Predictor_regressor")
def fire_predictor_regressor():
        # Load the pipeline
    

    # New sample (must match the original column order and types)
    sample = [[334.0961,	-117.5279,	301.4,	1	,1,	289.6	,3.3,	'D' ,	2	, 19,	171	, 'Degrees Compass'	,1]]  # 13 columns

    # Predict
    prediction = regressor.predict(sample)
   



    print(prediction)

    return jsonify(prediction=prediction.tolist())

@app.route("/fire_Predictor_Classifier")
def fire_predictor_Classifier():
    

    #update to take in input
    sample = [[36.6853	,-119.6669,371.9,1,1,291.4	,124.2,'D'	,0,	21 ,	193.6,	'Degrees Compass'	,0.1], 
            [33.9604,	-117.4206,317.2,1.5,1.2	,291.5,	22.5,'D'	,2	,18 ,	0.7	,'Knots',	0.1], 
            [33.2066 ,-117.3809,303.1,1.1,1,289.6,4.8,'D',2,19,21	,'Degrees Compass',	0.1	]
            ]  # 12 columns

    # Predict
    prediction = classifier.predict(sample)


    print(prediction)

    return jsonify(prediction=prediction.tolist())
