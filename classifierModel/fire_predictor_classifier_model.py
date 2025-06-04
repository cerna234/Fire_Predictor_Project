from joblib import load

# Load the pipeline
pipeline = load(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\classifierModel\model_20250603_141004.joblib')

# New sample (must match the original column order and types)
sample = [[36.6853	,-119.6669,371.9,1,1,291.4	,124.2,'D'	,0,	21 ,	193.6 ,0.1], 
       
        ]  # 12 columns

# Predict
prediction = pipeline.predict(sample)


print(prediction)
