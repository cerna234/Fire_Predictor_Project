import pandas as pd
import numpy as np
from datetime import datetime


def convertData(columns_to_remove,file_Name):


   
   
    data = pd.read_csv(file_Name)

    #Remove unwanted columns
    columns_to_drop = columns_to_remove
    data = data.drop(columns=columns_to_drop)
    # Step 3: Export to CSV

   
      
    #data.to_csv(f'{typeOfData}_{year}_data(convertedTimes).csv', index=False)

    return data

def filter_data(data,state_to_filter,name_of_state_column,year,typeOfData):

    state = state_to_filter
    data =  data[data[name_of_state_column] == state].copy()
    
    # Get unique records (remove duplicates)
    data = data.drop_duplicates(subset=['Latitude', 'Longitude', 'Date Local', 'Time Local', 'State Name', 'County Name'])


    
    return data


def combine_files(file1,file2):


    
     
    file1 = file1.rename(columns={'Sample Measurement': 'Temperature'})
    file2 = file2.rename(columns={'Sample Measurement': 'WindSpeed'})




    print(file1)
    print(file2)

    merged_df = pd.merge(
    file1,
    file2,
    on=['Latitude', 'Longitude', 'Date Local', 'Time Local', 'State Name', 'County Name'],
    how='inner'  # use 'outer' if you want all records from both files
    )

    merged_df.to_csv(f'data(convertedTimes).csv', index=False)
   


def main():
        # Convert Wind File
    year_file = 2024
    convertedWindData = convertData(
        columns_to_remove=[
        'State Code', 'County Code', 'Site Num', 'Parameter Code', 'POC',
        'Datum', 'Parameter Name', 'Date GMT', 'Time GMT',
        'Units of Measure', 'MDL', 'Qualifier', 
        'Method Type', 'Method Code', 'Method Name', 
        'Date of Last Change'
        ],
        file_Name= fr'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\DataFiles\WeatherData\hourly_WIND_2024.csv',
      
        
    )

    year_file = 2024
    convertedTempData = convertData(
        columns_to_remove=[
        'State Code', 'County Code', 'Site Num', 'Parameter Code', 'POC',
        'Datum', 'Parameter Name', 'Date GMT', 'Time GMT',
        'Units of Measure', 'MDL', 'Qualifier', 
        'Method Type', 'Method Code', 'Method Name', 
        'Date of Last Change'
        ],
        file_Name= fr'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\DataFiles\WeatherData\hourly_TEMP_2024.csv',
      
        
    )

    windFilterdData = filter_data(
        data = convertedWindData,
        state_to_filter = "California",
        name_of_state_column = "State Name",
        year = 2024,
        typeOfData = "wind"
    )


    tempFilteredData = filter_data(
        data = convertedTempData,
        state_to_filter = "California",
        name_of_state_column = "State Name",
        year = 2024,
        typeOfData = "temp"
    )
    # Convert Fire File
   
    combine_files(tempFilteredData,windFilterdData)

main()


#dtWeather = pd.read_csv(fr"C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\DataFiles\WeatherData\hourly_WIND_2024.csv")



#print(dtWeather)



#dtTemp = pd.read_csv(fr"C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\DataFiles\WeatherData\hourly_TEMP_2024.csv")

#print(dtTemp)