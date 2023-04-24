from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plot
from datetime import datetime
PATH = 'd:/workspace/Airline/github_practice/state_modified.csv'

train_data_copy = pd.read_csv(PATH)

print(train_data_copy.head())
def format_number(num):
    if pd.isna(num):
        return None
    if num == '0' or num == 2400:
        return '00:00'
    elif isinstance(num, float) or isinstance(num,int):
        num = int(num)
    return '{:04d}'.format(num)

def format_time(string):
    if pd.isna(string):
        return None
    # elif len(string) < 5:
    else:
        time = string[:2]+':'+string[2:]
        return time
def replace_none_with_depart_mode(group):
    group_med = group['Estimated_Departure_Time'].mode()
    group['Estimated_Departure_Time'].fillna(group_med, inplace=True)
    return group

def replace_none_with_arrival_mode(group):
    group_med = group['Estimated_Arrival_Time'].mode()
    group['Estimated_Arrival_Time'].fillna(group_med, inplace=True)
    return group

train_data_copy = train_data_copy.groupby(['Month','Origin_Airport','Destination_Airport','Distance', 'Airline','Tail_Number']).apply(replace_none_with_depart_mode).reset_index(drop=True)
train_data_copy = train_data_copy.groupby(['Month','Origin_Airport','Destination_Airport','Distance', 'Airline','Tail_Number']).apply(replace_none_with_arrival_mode).reset_index(drop=True)  
    

    
train_data_copy['Estimated_Departure_Time']=train_data_copy['Estimated_Departure_Time'].apply(format_number)
train_data_copy['Estimated_Arrival_Time']=train_data_copy['Estimated_Arrival_Time'].apply(format_number)
train_data_copy['Estimated_Departure_Time']=train_data_copy['Estimated_Departure_Time'].apply(format_time)
train_data_copy['Estimated_Arrival_Time']=train_data_copy['Estimated_Arrival_Time'].apply(format_time)
print(train_data_copy[['Estimated_Departure_Time','Estimated_Arrival_Time']])

# train_data_copy[['Estimated_Departure_Time','Estimated_Arrival_Time']] = train_data_copy[['Estimated_Departure_Time','Estimated_Arrival_Time']].astype(str)
# train_data_copy['Estimated_Arrival_Time'].replace('nan',pd.NA,inplace=True)
# train_data_copy['Estimated_Departure_Time'].replace('nan',pd.NA,inplace=True)

print(train_data_copy['Estimated_Arrival_Time'].head())
print(train_data_copy.isna().sum())
# 지연되지 않은 항공편 정보만 추출
train_not_delayed = train_data_copy.loc[train_data_copy['Delay_Not_Delayed']==1,['index', 'ID', 'Month', 'Day_of_Month', 'Estimated_Departure_Time',
       'Estimated_Arrival_Time', 'Cancelled', 'Diverted', 'Origin_Airport',
       'Origin_Airport_ID', 'Origin_State', 'Destination_Airport',
       'Destination_Airport_ID', 'Destination_State', 'Distance', 'Airline',
       'Carrier_Code(IATA)', 'Carrier_ID(DOT)', 'Tail_Number', 'Delay_Delayed',
       'Delay_Not_Delayed']]
train_not_delayed.reset_index(drop=False,inplace=True)
train_not_delayed.drop(columns='level_0',inplace=True)


# train_data_copy['Estimated_Departure_Time']=pd.to_datetime(train_data_copy['Estimated_Departure_Time'],format='%H:%M').dt.time
# train_data_copy['Estimated_Arrival_Time']=pd.to_datetime(train_data_copy['Estimated_Arrival_Time'],format='%H:%M').dt.time





# test = train_data_copy.drop_duplicates(subset=['Estimated_Departure_Time','Estimated_Arrival_Time','Distance','Origin_Airport','Destination_Airport','Carrier_ID(DOT)','Tail_Number'])

# test_arr = test.dropna(subset=['Estimated_Arrival_Time','level_0'])

# print(train_not_delayed.duplicated(subset = ['Distance','Origin_Airport','Destination_Airport','Carrier_ID(DOT)','Tail_Number']))
# print(train_not_delayed.isna().sum())
dup_dep = train_data_copy.duplicated(subset=['Estimated_Departure_Time','Distance','Origin_Airport','Destination_Airport','Carrier_ID(DOT)','Tail_Number'])
# for i in range(len(dup_dep)):
#     if not dup_dep[i]:
#         print(train_not_delayed['Estimated_Arrival_Time'][i])

def show_duplicates(group):
    if len(group)>1:
        return group






duplicated_groups = train_data_copy.groupby(['Month','Distance','Origin_Airport','Destination_Airport','Carrier_ID(DOT)','Tail_Number','Day_of_Month'], as_index=False).apply(show_duplicates)


print(duplicated_groups[['Month','Estimated_Departure_Time','Estimated_Arrival_Time','Origin_Airport','Destination_Airport','Airline','Tail_Number','Day_of_Month']])



# print(train_data_copy['Estimated_Arrival_Time'][train_data_copy[train_data_copy['Estimated_Departure_Time']==600].index])
print(train_data_copy.isna().sum())
print(type(train_data_copy['Estimated_Arrival_Time'][1]))
# print(test['Estimated_Arrival_Time'][test[test['Estimated_Arrival_Time']].index])
# train_not_delayed['Estimated_Arrival_Time'][train_not_delayed[]]

train_data_copy.to_csv('preprocessed.csv',index=False)

# print(train_not_delayed.duplicated(subset=['Estimated_Departure_Time','Distance','Origin_Airport','Destination_Airport']).sum())
