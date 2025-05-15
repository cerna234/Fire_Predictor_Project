import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from joblib import dump

dataset = pd.read_csv(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\2020\combinedFiles_classification(20250514_162355)2020.csv')

dataset['date_Time_fireFile'] = pd.to_datetime(dataset['date_Time_fireFile'])

dataset['date_Time_fireFile'] = dataset['date_Time_fireFile'].dt.hour
print(dataset['date_Time_fireFile'])

x = dataset.iloc[:,:-1].values


y = dataset.iloc[:,-1].values

# Define categorical columns for encoding (by column index or name)
categorical_features = [7, 9,11]  # Adjust based on your actual dataset


# Preprocessing transformer
preprocessor = ColumnTransformer(
    transformers=[('encoder', OneHotEncoder(), categorical_features)],
    remainder='passthrough'
)

# Pipeline: Preprocessing + Model
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor(n_estimators=100, random_state=0))
])


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)



# Train/test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)




classifier = RandomForestClassifier()

pipeline.fit(x_train, y_train)

print(pipeline.predict(x_test))

dump(pipeline, 'fire_predictor_pipeline_Classifier.joblib')





