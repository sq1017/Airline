import pandas as pd
from datetime import datetime


data = pd.read_csv('/home/park/workspace_github/github_practice/final_time_modified.csv')


data_copy = data.copy()


data_copy['Estimated_Departure_Datetime'].replace("['Estimated_Departure_Datetime']",None,inplace=True)


data_copy['Estimated_Departure_Datetime']=pd.to_datetime(data_copy['Estimated_Departure_Datetime'])
data_copy['Estimated_Arrival_Datetime']=pd.to_datetime(data_copy['Estimated_Arrival_Datetime'])
data_copy['Elapsed_Time']=pd.to_timedelta(data_copy['Elapsed_Time'])

print(data_copy)


data_copy['Estimated_Arrival_Datetime'] = data_copy.apply(lambda row: row['Estimated_Departure_Datetime'] + row['Elapsed_Time'] if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Arrival_Datetime'],axis = 1)

data_copy['Estimated_Departure_Datetime'] = data_copy.apply(lambda row: row['Estimated_Arrival_Datetime'] - row['Elapsed_Time'] if (not pd.isna(row['Estimated_Arrival_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Departure_Datetime'],axis = 1)

data_copy['Estimated_Departure_Time'] = data_copy.apply(lambda row: datetime.time(row['Estimated_Departure_Datetime']) if (not pd.isna(row['Estimated_Departure_Datetime'])) else row['Estimated_Departure_Time'],axis=1)

data_copy['Estimated_Arrival_Time'] = data_copy.apply(lambda row: datetime.time(row['Estimated_Arrival_Datetime']) if (not pd.isna(row['Estimated_Arrival_Datetime'])) else row['Estimated_Arrival_Time'],axis=1)

print(data_copy.isna().sum())