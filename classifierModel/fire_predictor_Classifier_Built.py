from joblib import load

# Load the pipeline
pipeline = load(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\classifierModel\fire_predictor_pipeline_Classifier.joblib')

# New sample (must match the original column order and types)
sample = [[36.6853	,-119.6669,371.9,1,1,291.4	,124.2,'D'	,0,	21 ,	193.6,	'Degrees Compass'	,0.1], 
          [33.9604,	-117.4206,317.2,1.5,1.2	,291.5,	22.5,'D'	,2	,18 ,	0.7	,'Knots',	0.1], 
          [33.2066 ,-117.3809,303.1,1.1,1,289.6,4.8,'D',2,19,21	,'Degrees Compass',	0.1	]
        ]  # 12 columns

# Predict
prediction = pipeline.predict(sample)


print(prediction)
