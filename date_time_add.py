import pandas as pd
from datetime import datetime,timedelta
import numpy as np

data = pd.read_csv('d:/workspace/Airline/github_practice/state_modified.csv')

data_copy = data.copy()



def time_format_change(num):
    if pd.isna(num):
        return None
    else :
        num = int(num)
        if num == 2400:
            return '0000' 
        return '{:04d}'.format(num)
    

data_copy['Estimated_Departure_Time']=data_copy['Estimated_Departure_Time'].apply(time_format_change)
data_copy['Estimated_Arrival_Time']=data_copy['Estimated_Arrival_Time'].apply(time_format_change)


def create_departure_timedate(group): # datetime format을 맞추기 위해 임의로 연도를 2022년으로 설정
    if pd.isna(group['Estimated_Departure_Time']):
        group['Estimated_Departure_Datetime'] = pd.NaT
        return group
    else :
        group['Estimated_Departure_Datetime'] = datetime(year=2022,month=group['Month'],day=group['Day_of_Month'],hour=int(group['Estimated_Departure_Time'][:2]),minute=int(group['Estimated_Departure_Time'][2:]))
        return group
    
def create_arrival_timedate(group):
    if pd.isna(group['Estimated_Arrival_Time']):
        group['Estimated_Arrival_Datetime'] = pd.NaT
        return group
    else :    
        group['Estimated_Arrival_Datetime'] = datetime(year=2022,month=group['Month'],day=group['Day_of_Month'],hour=int(group['Estimated_Arrival_Time'][:2]),minute=int(group['Estimated_Arrival_Time'][2:]))
        return group

data_copy = data_copy.apply(create_departure_timedate,axis=1)
data_copy = data_copy.apply(create_arrival_timedate,axis=1)
data_copy

data_copy['Estimated_Arrival_Datetime'] = data_copy.apply(lambda row: row['Estimated_Arrival_Datetime'] + timedelta(days=1) if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Estimated_Arrival_Datetime'])) and (row['Estimated_Departure_Datetime'] > row['Estimated_Arrival_Datetime']) else row['Estimated_Arrival_Datetime'], axis=1)



data_copy.to_csv(path_or_buf='d:/workspace/Airline/github_practice/date_time_column_added.csv')