import pandas as pd
from datetime import datetime

data = pd.read_csv('/home/park/workspace_github/github_practice/final_time_modified_day24.csv')
data_copy = data.copy()
data_copy['Estimated_Departure_Datetime']=pd.to_datetime(data_copy['Estimated_Departure_Datetime'])
data_copy['Estimated_Arrival_Datetime']=pd.to_datetime(data_copy['Estimated_Arrival_Datetime'])
data_copy['Elapsed_Time']=pd.to_timedelta(data_copy['Elapsed_Time'])

def fill_elapsed(group):
    elapsed_mean = group['Elapsed_Time'].mean()
    group['Elapsed_Time'].fillna(elapsed_mean,inplace=True)
    return group

data_copy = data_copy.groupby(['Origin_Airport','Destination_Airport','Airline']).apply(fill_elapsed).reset_index(drop=True)

data_copy = data_copy.groupby(['Origin_Airport','Destination_Airport','Distance']).apply(fill_elapsed).reset_index(drop=True)


data_copy['Estimated_Arrival_Datetime'] = data_copy.apply(lambda row: row['Estimated_Departure_Datetime'] + row['Elapsed_Time'] if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Arrival_Datetime'],axis = 1)

data_copy['Estimated_Departure_Datetime'] = data_copy.apply(lambda row : row['Estimated_Arrival_Datetime'] - row['Elapsed_Time'] if (not pd.isna(row['Estimated_Arrival_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Departure_Datetime'],axis = 1)

data_copy['Estimated_Arrival_Datetime'] = data_copy.apply(lambda row: row['Estimated_Departure_Datetime'] + row['Elapsed_Time'] if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Arrival_Datetime'],axis = 1)

data_copy['Estimated_Departure_Datetime'] = data_copy.apply(lambda row : row['Estimated_Arrival_Datetime'] - row['Elapsed_Time'] if (not pd.isna(row['Estimated_Arrival_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Departure_Datetime'],axis = 1)

data_copy['Estimated_Arrival_Datetime'] = data_copy.apply(lambda row: row['Estimated_Departure_Datetime'] + row['Elapsed_Time'] if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Arrival_Datetime'],axis = 1)

data_copy['Estimated_Departure_Datetime'] = data_copy.apply(lambda row : row['Estimated_Arrival_Datetime'] - row['Elapsed_Time'] if (not pd.isna(row['Estimated_Arrival_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Departure_Datetime'],axis = 1)

data_copy['Estimated_Arrival_Datetime'] = data_copy.apply(lambda row: row['Estimated_Departure_Datetime'] + row['Elapsed_Time'] if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Arrival_Datetime'],axis = 1)

data_copy['Estimated_Departure_Datetime'] = data_copy.apply(lambda row : row['Estimated_Arrival_Datetime'] - row['Elapsed_Time'] if (not pd.isna(row['Estimated_Arrival_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Departure_Datetime'],axis = 1)

data_copy['Estimated_Arrival_Time'] = data_copy.apply(lambda row: datetime.time(row['Estimated_Arrival_Datetime']) if (not pd.isna(row['Estimated_Arrival_Datetime'])) else row['Estimated_Arrival_Time'],axis=1)

data_copy['Estimated_Departure_Time'] = data_copy.apply(lambda row: datetime.time(row['Estimated_Departure_Datetime']) if (not pd.isna(row['Estimated_Departure_Datetime'])) else row['Estimated_Departure_Time'],axis=1)



print(data_copy.isna().sum())

data_copy.to_csv('/home/park/workspace_github/github_practice/time_end.csv')