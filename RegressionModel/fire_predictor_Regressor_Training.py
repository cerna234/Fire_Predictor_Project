import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from joblib import dump

# Load dataset
dataset = pd.read_csv(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\2020\combinedFiles_regression(20250514_162343)2020.csv')

dataset['date_Time_fireFile'] = pd.to_datetime(dataset['date_Time_fireFile'])
dataset['date_Time_fireFile'] = dataset['date_Time_fireFile'].dt.hour


# Features and labels
x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

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

# Train/test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Fit pipeline
pipeline.fit(x_train, y_train)

print(pipeline.predict(x_test))



# Save the entire pipeline
dump(pipeline, 'fire_predictor_pipeline.joblib')
