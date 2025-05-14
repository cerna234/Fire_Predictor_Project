import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor


dataset = pd.read_csv('combinedFiles_regression(20250513_155748).csv')




x = dataset.iloc[:,:-1].values


y = dataset.iloc[:,-1].values


#Encoded text columns
ct = ColumnTransformer(transformers=  [('encoder',OneHotEncoder(), [7,10] )] ,remainder='passthrough')
x = np.array(ct.fit_transform(x)) #returns output of matrix of feature x




x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)






regressor = RandomForestRegressor(n_estimators=100, random_state=0)
regressor.fit(x_train, y_train)
y_pred = regressor.predict(x_test)




for i in range(len(y_pred)):
   
    print(f'PREDICTIONS: {y_pred[i]}  ACTUAL: {y_test[i]}')


