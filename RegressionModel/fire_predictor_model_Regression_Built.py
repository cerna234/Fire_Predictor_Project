from joblib import load

# Load the pipeline
pipeline = load(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\RegressionModel\fire_predictor_pipeline.joblib')

# New sample (must match the original column order and types)
sample = [[334.0961,	-117.5279,	301.4,	1	,1,	289.6	,3.3,	'D' ,	2	, 19,	171	, 'Degrees Compass'	,1]]  # 13 columns

# Predict
prediction = pipeline.predict(sample)
print(prediction)
