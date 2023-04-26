from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plot
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
from datetime import datetime,timedelta
import math



data = pd.read_csv('/content/drive/MyDrive/state_modified.csv')

data_copy = data.copy()


data_copy.dropna(subset=['Delay'],inplace=True) # Delay 컬럼의 결측치가 포함된 열 전부 제거
data_copy.reset_index(drop=False,inplace=True) # 제거된 열로 인해 번호가 안맞는 index 재설정

data_copy = pd.get_dummies(data_copy,columns=['Delay'])

# bool형인 종속변수는 int형으로
data_copy['Delay_Delayed'] = data_copy['Delay_Delayed'].astype(int)
data_copy['Delay_Not_Delayed'] = data_copy['Delay_Not_Delayed'].astype(int)

# 주(state) 결측값 채우기
########################################################################
def fill_origin_state(group):
    group_sort = group[group['Origin_State'].notna().sort_values(ascending=False)]['Origin_State']
    group_sort.reset_index(drop=True,inplace=True)
    group['Origin_State'].fillna(group_sort[0],inplace=True)
    return group
def fill_destination_state(group):
    group_sort = group[group['Destination_State'].notna().sort_values(ascending=False)]['Destination_State']
    group_sort.reset_index(drop=True,inplace=True)
    group['Destination_State'].fillna(group_sort[0],inplace=True)
    return group

data_copy = data_copy.groupby(['Origin_Airport']).apply(fill_origin_state).reset_index(drop=True)
data_copy = data_copy.groupby(['Destination_Airport']).apply(fill_destination_state).reset_index(drop=True)
########################################################################


# 시간 결측값 학습 + 예측
#############################################################################
# OPEN file : train.csv


# extract data of time and distance
target_data=['Estimated_Departure_Time','Estimated_Arrival_Time','Distance']
time_distance=data_copy[target_data]
time_distance.dropna(subset=['Estimated_Arrival_Time'], inplace=True)

# index list of departure_time isnull()
index_dep=time_distance[time_distance['Estimated_Departure_Time'].isna()].index

# dataframe of departure_time isnull()
departure_data=time_distance.loc[index_dep]

# drop remaining NaN values to operate modeling
time_distance.dropna(inplace=True)

# training
y=time_distance.pop('Estimated_Departure_Time')
X=time_distance
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)

# modeling
model_dep=RandomForestRegressor()
model_dep.fit(X_train, y_train)

# modeling check
pred=model_dep.predict(X_test)
r2_score(y_test, pred)

# project NaN data of Departure Time
departure_data_bak=departure_data.copy()
dep_y=departure_data.pop('Estimated_Departure_Time')
dep_X=departure_data
pred=model_dep.predict(dep_X)
departure_data_bak['Estimated_Departure_Time']=pred

# fill the estimated departure_time_data to original dataframe
data_copy.loc[departure_data_bak.index, 'Estimated_Departure_Time']=departure_data_bak['Estimated_Departure_Time']

# OPEN file : train.csv
# data_copy=pd.read_csv('./open/train.csv')

# extract data of time and distance
target_data=['Estimated_Departure_Time','Estimated_Arrival_Time','Distance']
time_distance=data_copy[target_data]
time_distance.dropna(subset=['Estimated_Departure_Time'], inplace=True)

# index list of arrival_time isnull()
index_dep=time_distance[time_distance['Estimated_Arrival_Time'].isna()].index

# dataframe of arrival_time isnull()
departure_data=time_distance.loc[index_dep]

# drop remaining NaN values to operate modeling
time_distance.dropna(inplace=True)

# training
y=time_distance.pop('Estimated_Arrival_Time')
X=time_distance
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)

# modeling
model_dep=RandomForestRegressor()
model_dep.fit(X_train, y_train)

# modeling check
pred=model_dep.predict(X_test)
r2_score(y_test, pred)

# project NaN data of Arrival Time
departure_data_bak=departure_data.copy()
dep_y=departure_data.pop('Estimated_Arrival_Time')
dep_X=departure_data
pred=model_dep.predict(dep_X)
departure_data_bak['Estimated_Arrival_Time']=pred

# fill the estimated arrival_time_data to original dataframe
data_copy.loc[departure_data_bak.index, 'Estimated_Arrival_Time']=departure_data_bak['Estimated_Arrival_Time']
print(data_copy.isna().sum())

###############################################################################################

# 시간 계산을 편하게 하기 위해 출발 시간과 도착 시간에 따른 시간형 데이터 컬럼 /걸린 시간 컬럼 생성
##############################################################################################
def to_int(num):
  if pd.isna(num):
    return pd.NaT
  else:
    return int(num)


def time_format_change(num):
    if pd.isna(num):
        return None
    else :
        num = int(num)
        if num == 2400:
            return '0000' 
        a = '{:04d}'.format(num)
        temp = list(a)
        if '6' <= temp[2] <='9':
          temp[2] = '0'
          temp[1] = str(int(temp[1])+1)
          output = "".join(temp)
          return output

        # if temp[2] == '6':
        #   temp[2] = '0'
        #   temp[1] = str(int(temp[1])+1)
        #   output = "".join(temp)
        #   return output
        # if temp[2] == '7':
        #   temp[2] = '1'
        #   temp[1] = str(int(temp[1])+1)
        #   output = "".join(temp)
        #   return output
        # if temp[2] == '8':
        #   temp[2] = '2'
        #   temp[1] = str(int(temp[1])+1)
        #   output = "".join(temp)
        #   return output
        # if temp[2] == '9':
        #   temp[2] = '3'
        #   temp[1] = str(int(temp[1])+1)
        #   output = "".join(temp)
        #   return output
        else:
          return a

data_copy['Estimated_Departure_Time'] = data_copy['Estimated_Departure_Time'].apply(to_int)
data_copy['Estimated_Arrival_Time'] = data_copy['Estimated_Departure_Time'].apply(to_int)

print(data_copy.isna().sum())


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

data_copy['Estimated_Arrival_Datetime'] = data_copy.apply(lambda row: row['Estimated_Arrival_Datetime'] + timedelta(days=1) if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Estimated_Arrival_Datetime'])) and (row['Estimated_Departure_Datetime'] > row['Estimated_Arrival_Datetime']) else row['Estimated_Arrival_Datetime'], axis=1)


data_copy['Estimated_Departure_Datetime']=pd.to_datetime(data_copy['Estimated_Departure_Datetime'])
data_copy['Estimated_Arrival_Datetime']=pd.to_datetime(data_copy['Estimated_Arrival_Datetime'])
data_copy['Elapsed_Time'] = data_copy.apply(lambda row: row['Estimated_Arrival_Datetime'] - row['Estimated_Departure_Datetime'] if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Estimated_Arrival_Datetime'])) else pd.NaT, axis=1)

############################################################################################################


# 걸린 시간 컬럼의 결측값을 동일한 운행을 하는 항공편들의 평균값으로 설정
#############################################################################################################
def fill_elapsed(group):
    elapsed_mean = group['Elapsed_Time'].mean()
    group['Elapsed_Time'].fillna(elapsed_mean,inplace=True)
    return group

data_copy = data_copy.groupby(['Month','Origin_Airport','Destination_Airport','Distance', 'Airline','Tail_Number']).apply(fill_elapsed).reset_index(drop=True)

data_copy = data_copy.groupby(['Month','Origin_Airport','Destination_Airport','Distance', 'Airline']).apply(fill_elapsed).reset_index(drop=True)

data_copy = data_copy.groupby(['Month','Origin_Airport','Destination_Airport','Distance']).apply(fill_elapsed).reset_index(drop=True)

data_copy = data_copy.groupby(['Origin_Airport','Destination_Airport','Distance','Airline']).apply(fill_elapsed).reset_index(drop=True)

data_copy = data_copy.groupby(['Origin_Airport','Destination_Airport','Airline']).apply(fill_elapsed).reset_index(drop=True)

data_copy = data_copy.groupby(['Origin_Airport','Destination_Airport','Distance']).apply(fill_elapsed).reset_index(drop=True)


data_copy['Estimated_Arrival_Datetime'] = data_copy.apply(lambda row: row['Estimated_Departure_Datetime'] + row['Elapsed_Time'] if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Arrival_Datetime'],axis = 1)

data_copy['Estimated_Departure_Datetime'] = data_copy.apply(lambda row: row['Estimated_Arrival_Datetime'] - row['Elapsed_Time'] if (not pd.isna(row['Estimated_Arrival_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Departure_Datetime'],axis = 1)

data_copy['Estimated_Arrival_Datetime'] = data_copy.apply(lambda row: row['Estimated_Departure_Datetime'] + row['Elapsed_Time'] if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Arrival_Datetime'],axis = 1)

data_copy['Estimated_Departure_Datetime'] = data_copy.apply(lambda row : row['Estimated_Arrival_Datetime'] - row['Elapsed_Time'] if (not pd.isna(row['Estimated_Arrival_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Departure_Datetime'],axis = 1)

data_copy['Estimated_Arrival_Datetime'] = data_copy.apply(lambda row: row['Estimated_Departure_Datetime'] + row['Elapsed_Time'] if (not pd.isna(row['Estimated_Departure_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Arrival_Datetime'],axis = 1)

data_copy['Estimated_Departure_Datetime'] = data_copy.apply(lambda row : row['Estimated_Arrival_Datetime'] - row['Elapsed_Time'] if (not pd.isna(row['Estimated_Arrival_Datetime'])) and (not pd.isna(row['Elapsed_Time'])) else row['Estimated_Departure_Datetime'],axis = 1)

# data_copy['Estimated_Arrival_Time'] = data_copy.apply(lambda row: datetime.time(row['Estimated_Arrival_Datetime']) if (not pd.isna(row['Estimated_Arrival_Datetime'])) else row['Estimated_Arrival_Time'],axis=1)

# data_copy['Estimated_Departure_Time'] = data_copy.apply(lambda row: datetime.time(row['Estimated_Departure_Datetime']) if (not pd.isna(row['Estimated_Departure_Datetime'])) else row['Estimated_Departure_Time'],axis=1)
#################################################################################

# 원활한 학습을 위해 시간 데이터를 각 요소 별로 정수형으로 분리
##############################################################################

data_copy['E_D_M'] = data_copy.apply(lambda row : row['Estimated_Departure_Datetime'].month,axis=1)
data_copy['E_D_D'] = data_copy.apply(lambda row : row['Estimated_Departure_Datetime'].day,axis=1)
data_copy['E_D_H'] = data_copy.apply(lambda row : row['Estimated_Departure_Datetime'].hour,axis=1)
data_copy['E_D_m'] = data_copy.apply(lambda row : row['Estimated_Departure_Datetime'].minute,axis=1)

data_copy['E_A_M'] = data_copy.apply(lambda row : row['Estimated_Arrival_Datetime'].month,axis=1)
data_copy['E_A_D'] = data_copy.apply(lambda row : row['Estimated_Arrival_Datetime'].day,axis=1)
data_copy['E_A_H'] = data_copy.apply(lambda row : row['Estimated_Arrival_Datetime'].hour,axis=1)
data_copy['E_A_m'] = data_copy.apply(lambda row : row['Estimated_Arrival_Datetime'].minute,axis=1)

data_copy['Elapsed_Time'] = data_copy.apply(lambda row : row['Elapsed_Time'].seconds // 60 ,axis=1)
####################################################################################3

def airline_fillna(col1, col2):
    dt_array = data_copy[col1].dropna().unique()
    for i in dt_array:
        id = data_copy[data_copy[col1]==i][col2].dropna().unique()[0]
        data_copy.loc[data_copy[col1]==i, col2] = data_copy[data_copy[col1]==i][col2].fillna(id)

airline_fillna('Airline', 'Carrier_ID(DOT)')

# 1:1로 대응되는 Carrier_Code와 Carrier_ID 데이터를 이용하여 결측치 추가 제거(결측치: 2,185행)
for i in ['WN', 'NK', 'B6', 'F9', 'G4', 'VX']:
    id = data_copy[data_copy['Carrier_Code(IATA)']==i]['Carrier_ID(DOT)'].dropna().unique()[0]
    data_copy.loc[data_copy['Carrier_Code(IATA)']==i, 'Carrier_ID(DOT)'] = data_copy[data_copy['Carrier_Code(IATA)']==i]['Carrier_ID(DOT)'].fillna(id)

# carrier_id 결측치(2,185행) 삭제
data_copy = data_copy.dropna(subset=['Carrier_ID(DOT)'], axis=0).reset_index(drop=True)

# origin_state / destination_state / tail_number 인코딩
le = LabelEncoder()
data_copy_tail = le.fit_transform(data_copy['Tail_Number'])
data_copy_or = le.fit_transform(data_copy['Origin_State'])
data_copy_de = le.fit_transform(data_copy['Destination_State'])
data_copy_le = pd.DataFrame({'tail_num': data_copy_tail, 'origin_st':data_copy_or, 'destination_st':data_copy_de})

data = pd.concat([data_copy, data_copy_le], axis=1)






# 필요 없는 컬럼 삭제
data_copy.drop(['Airline', 'Carrier_Code(IATA)'], axis=1, inplace=True)
data_copy.drop(['Cancelled', 'Diverted', 'Origin_Airport', 'Destination_Airport', 'Delay_Not_Delayed'], axis=1, inplace=True)
data_copy.drop(['ID', 'Origin_State', 'Destination_State'], axis=1, inplace=True)
data_copy.drop(['Estimated_Arrival_Time','Estimated_Departure_Time,Estimated_Arrival_Datetime','Estimated_Departure_Datetime','Month','Day_of_Month'],axis=1,inplace=True)





data_copy.to_csv('preproecessed_1.csv')

