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

dataset = pd.read_csv(r'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\2023\combinedFiles_classification(20250513_211640)2023.csv')




x = dataset.iloc[:,:-1].values


y = dataset.iloc[:,-1].values


#Encoded text columns
ct = ColumnTransformer(transformers=  [('encoder',OneHotEncoder(), [7,10] )] ,remainder='passthrough')
x = np.array(ct.fit_transform(x)) #returns output of matrix of feature x




x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)





classifier = RandomForestClassifier()

model = classifier.fit(x_train,y_train)

y_pred = model.predict(x_test)




for i in range(len(y_pred)):
   
    print(f'PREDICTIONS: {y_pred[i]}  ACTUAL: {y_test[i]}')


mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
