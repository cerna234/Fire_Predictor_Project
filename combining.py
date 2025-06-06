import pandas as pd
import numpy as np
from datetime import datetime





def convertData(columns_to_remove,column_to_combine,column_to_combine_2,new_column_Name,file_Name,state_to_filter,name_of_state_column,year,typeOfData):


   
   
    data = pd.read_csv(file_Name)


 


    #make time columns match same format


    #Date Columns


    #Fire File
    if state_to_filter == '':


        data.rename(columns={'latitude': 'Latitude', 'longitude': 'Longitude'}, inplace=True)


        formatted_times = []
        for date in data[column_to_combine_2]:
       
            time_str = f"{date:04d}"
            formatted_time = f"{time_str[:2]}:{time_str[2:]}"
            formatted_times.append(formatted_time)




           


        data[column_to_combine_2] = formatted_times






   
   
    if state_to_filter != '':


        state = state_to_filter
        data =  data[data[name_of_state_column] == state].copy()


   
   
  # Step 2: Add datetime_local column
    data[new_column_Name] = data[column_to_combine] + ' ' + data[column_to_combine_2]
    data[new_column_Name] = pd.to_datetime(data[new_column_Name])
    data[new_column_Name] = data[new_column_Name].dt.round('h')
    year = year




    #Remove unwanted columns
    columns_to_drop = columns_to_remove
    data = data.drop(columns=columns_to_drop)


    # Step 3: Export to CSV


    #Exports dataset with local date and time combined
    #Filters for Specified State
    fileNameGenerated = ''
   
    if state_to_filter != '':
        fileNameGenerated = f'{state}_{typeOfData}_{year}_data(convertedTimes).csv'
        data.to_csv(f'{state}_{typeOfData}_{year}_data(convertedTimes).csv', index=False)


    else:
        fileNameGenerated = f'{typeOfData}_{year}_data(convertedTimes).csv'
        data.to_csv(f'{typeOfData}_{year}_data(convertedTimes).csv', index=False)


   
    return fileNameGenerated
   




#v2


def combineFiles(isRegression,fireFile,windFile):




    #fireData = pd.read_csv('Fire_2023_data(convertedTimes).csv')
    fireData = pd.read_csv(fireFile)
   
    #wind_Data = pd.read_csv('California_Wind_2023_data(convertedTimes).csv')
    wind_Data = pd.read_csv(windFile)






    # Convert datetime to datetime objects
    fireData['date_Time'] = pd.to_datetime(fireData['date_Time'])
    wind_Data['date_Time'] = pd.to_datetime(wind_Data['date_Time'])


    # Round coordinates (e.g., to 3 decimal places ~111 meters)
    fireData['lat_rounded'] = fireData['Latitude'].round(1)
    fireData['lon_rounded'] = fireData['Longitude'].round(1)
    wind_Data['lat_rounded'] = wind_Data['Latitude'].round(1)
    wind_Data['lon_rounded'] = wind_Data['Longitude'].round(1)


    # Round datetime to the nearest minute (or 30 seconds, hour, etc.)
    fireData['time_rounded'] = fireData['date_Time'].dt.round('1min')
    wind_Data['time_rounded'] = wind_Data['date_Time'].dt.round('1min')


   
    # Merge on the rounded fields
    merged = pd.merge(fireData, wind_Data, on=['lat_rounded', 'lon_rounded', 'time_rounded'], how='inner', suffixes=('_fireFile', '_windFile'))



    columns_to_drop = ['Latitude_windFile','Longitude_windFile','date_Time_windFile','lat_rounded','lon_rounded','time_rounded','version', 'instrument', 'satellite',
    'State Code', 'County Code', 'Site Num', 'POC', 'Datum',
    'Parameter Name', 'Parameter Code',
    'Method Name', 'Method Code', 'Method Type',
    'Date of Last Change', 'Qualifier',
    'State Name', 'County Name','Uncertainty'
    ]
    merged = merged.drop(columns=columns_to_drop)
    filename = ''
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")



  
    merged = merged[merged['Units of Measure'] != "Degrees Compass"]

    merged["wind_measurements"] = merged["Sample Measurement"] * 1.15078






    grouped = (
    merged.groupby(["Latitude_fireFile", "Longitude_fireFile","brightness","scan","track","bright_t31","frp","daynight","type", "date_Time_fireFile","MDL","confidence"])["wind_measurements"]
    .agg(lambda x: x.dropna().max())
    .reset_index()
    )


    merged = grouped

    
    

# Step 4: (Optional) Merge back with original data if needed
# merged = pd.merge(...)

    

    '''
   
    '''
    if isRegression:
        merged['Chance_of_fire'] = merged['confidence']
        filename = f'combinedFiles_regression({timestamp}).csv'
    else:
        merged['fire_occurred'] = merged['confidence'].apply(lambda x: 1 if x >= 60 else 0)
        filename = f'combinedFiles_classification({timestamp}).csv'




    merged = merged.drop(columns='confidence')
   
    print(filename)
    merged.to_csv(filename, index=False)
   


   
   
 # Assuming 'merged' is your DataFrame


   
   
   




def main():
        # Convert Wind File
    year_file = 2021
    WindFileReturnFile =   convertData(
        columns_to_remove=['Date Local', 'Time Local', 'Date GMT', 'Time GMT'],
        column_to_combine='Date Local',
        column_to_combine_2='Time Local',
        new_column_Name='date_Time',
        file_Name= fr'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\DataFiles\{year_file}\hourly_WIND_{year_file}.csv',
        state_to_filter='California',
        name_of_state_column='State Name',
        year=year_file,
        typeOfData='Wind'
    )
 
    fireFileReturnFile = convertData(
        columns_to_remove=['acq_date', 'acq_time'],
        column_to_combine='acq_date',
        column_to_combine_2='acq_time',
        new_column_Name='date_Time',
        file_Name= fr'C:\Users\Miguel Cerna\OneDrive\Desktop\Fire_Predictor_Project\DataFiles\{year_file}\Fire_Data_{year_file}_United_States.csv',
        state_to_filter='',
        name_of_state_column='',
        year=year_file,
        typeOfData='Fire'
    )
    # Convert Fire File
   


    # Combine for Regression and Classification
    combineFiles(isRegression=True,fireFile=fireFileReturnFile,windFile=WindFileReturnFile)
    combineFiles(isRegression=False,fireFile=fireFileReturnFile,windFile=WindFileReturnFile)


main()
