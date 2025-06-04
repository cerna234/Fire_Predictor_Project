import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from joblib import dump
from datetime import datetime
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt


# Load dataset
dataset = pd.read_csv(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\DataFiles\FinalFiles\combinedFiles_regression(2017-2021).csv')

dataset['date_Time_fireFile'] = pd.to_datetime(dataset['date_Time_fireFile'])
dataset['date_Time_fireFile'] = dataset['date_Time_fireFile'].dt.day_of_week


# Features and labels
x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Define categorical columns for encoding (by column index or name)
categorical_features = [7]  # Adjust based on your actual dataset


# Preprocessing transformer
preprocessor = ColumnTransformer(
    transformers=[('encoder', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
    remainder='passthrough'
)

# Pipeline: Preprocessing + Model
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor(n_estimators=100, random_state=0))
])

# Train/test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Fit pipeline
pipeline.fit(x_train, y_train)

#print(pipeline.predict(x_test))




timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'model_{timestamp}.joblib'


'''
INPUTS
Latitude_fireFile|Longitude_fireFile|brightness|scan|track|bright_t31|frp|daynight|type|date_Time_fireFile|MDL|wind_measurements|

'''
y_pred = pipeline.predict(x_test)

dump(pipeline, filename)

'''
print("MAE:", mean_absolute_error(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R² Score:", r2_score(y_test, y_pred))



plt.figure(figsize=(8,6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--') 
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Predicted vs Actual')
plt.show()


'''
