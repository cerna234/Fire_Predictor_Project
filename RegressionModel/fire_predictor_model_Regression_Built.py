from joblib import load

# Load the pipeline
pipeline = load(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\RegressionModel\model_20250604_111457.joblib')

# New sample (must match the original column order and types)
sample = [[37.775, -122.4183, 315.36, 1.14, 1.07, 291.73, 15.28, 'D', 0, 3, 0.1, 11.3] ]  # 13 columns

# Predict
prediction = pipeline.predict(sample)
print(prediction)
