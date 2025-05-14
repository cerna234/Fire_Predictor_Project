from joblib import load

# Load the pipeline
pipeline = load(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\fire_predictor_pipeline.joblib')

# New sample (must match the original column order and types)
sample = [[32.7619 ,	-116.7775,	318.1,	3.3	,1.7	,300.3,	65.1,	'N'	,0,	1.6,	'Knots',	0.1]]  # 12 columns

# Predict
prediction = pipeline.predict(sample)
print(prediction)
