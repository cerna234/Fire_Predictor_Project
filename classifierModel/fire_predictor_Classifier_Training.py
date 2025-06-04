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
from datetime import datetime

dataset = pd.read_csv(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\DataFiles\FinalFiles\classification_Final_file.csv')

dataset['date_Time_fireFile'] = pd.to_datetime(dataset['date_Time_fireFile'])

dataset['date_Time_fireFile'] = dataset['date_Time_fireFile'].dt.hour


x = dataset.iloc[:,:-1].values

print(x)

y = dataset.iloc[:,-1].values


print(y)
# Define categorical columns for encoding (by column index or name)
categorical_features = [7]


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



timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'model_{timestamp}.joblib'


'''
INPUTS
Latitude_fireFile|Longitude_fireFile|brightness|scan|track|bright_t31|frp|daynight|type|date_Time_fireFile|MDL|wind_measurements|

'''
dump(pipeline, filename)






