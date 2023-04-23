import pandas as pd
from datetime import datetime

data = pd.read_csv('d:/workspace/Airline/github_practice/date_time_column_added.csv')

data.drop(columns='Unnamed: 0.1',inplace=True)
data.drop(columns='Unnamed: 0',inplace=True)


data_copy = data.copy()
data_copy['Estimated_Departure_Datetime']=pd.to_datetime(data_copy['Estimated_Departure_Datetime'])
data_copy['Estimated_Arrival_Datetime']=pd.to_datetime(data_copy['Estimated_Arrival_Datetime'])
data_copy['Elapsed_Time'] = data_copy.apply(lambda row: row['Estimated_Arrival_Datetime'] - row['Estimated_Departure_Datetime'] if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Estimated_Arrival_Datetime'])) else pd.NaT, axis=1)

def fill_elapsed(group):
    elapsed_mean = group['Elapsed_Time'].mean()
    group['Elapsed_Time'].fillna(elapsed_mean,inplace=True)
    return group

data_copy = data_copy.groupby(['Month','Origin_Airport','Destination_Airport','Distance', 'Airline','Tail_Number']).apply(fill_elapsed).reset_index(drop=True)

data_copy = data_copy.groupby(['Month','Origin_Airport','Destination_Airport','Distance', 'Airline']).apply(fill_elapsed).reset_index(drop=True)

data_copy = data_copy.groupby(['Month','Origin_Airport','Destination_Airport','Distance']).apply(fill_elapsed).reset_index(drop=True)

data_copy['Estimated_Arrival_Datetime'] = data_copy.apply(lambda row: row['Estimated_Departure_Datetime'] + row['Elapsed_Time'] if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Arrival_Datetime'],axis = 1)

data_copy['Estimated_Departure_Datetime'] = data_copy.apply(lambda row: row['Estimated_Arrival_Datetime'] - row['Elapsed_Time'] if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else ['Estimated_Departure_Datetime'],axis = 1)

data_copy['Estimated_Arrival_Time'] = data_copy.apply(lambda row: datetime.time(row['Estimated_Arrival_Datetime']) if (not pd.isna(row['Estimated_Arrival_Datetime'])) else row['Estimated_Arrival_Time'],axis=1)

# data_copy['Estimated_Departure_Time'] = data_copy.apply(lambda row: datetime.time(row['Estimated_Departure_Datetime']) if (not pd.isna(row['Estimated_Departure_Datetime'])) else row['Estimated_Departure_Time'],axis=1)


data_copy.to_csv('d:/workspace/Airline/github_practice/final_time_modified.csv')
