from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plot
import os


PATH = '/home/park/workspace_github/open/'
PATH_TRAIN = os.path.join(PATH,'train.csv')

train_data = pd.read_csv(PATH_TRAIN)

train_data_copy = train_data.copy()
train_data_copy.dropna(subset=['Delay'],inplace=True) # Delay 컬럼의 결측치가 포함된 열 전부 제거
train_data_copy.reset_index(drop=False,inplace=True) # 제거된 열로 인해 번호가 안맞는 index 재설정

train_data_copy = pd.get_dummies(train_data_copy,columns=['Delay'])

# bool형인 종속변수는 int형으로
train_data_copy['Delay_Delayed'] = train_data_copy['Delay_Delayed'].astype(int)
train_data_copy['Delay_Not_Delayed'] = train_data_copy['Delay_Not_Delayed'].astype(int)

train_data_copy[['Estimated_Departure_Time']]

print(train_data_copy['Origin_Airport'].value_counts().index[0])
print(train_data_copy['Origin_State'][train_data_copy[train_data_copy['Origin_Airport']=='ORD'].index])

train_data_copy.reset_index(drop=False,inplace=True)
print(train_data_copy.isna().sum())
class Autofill():
       def __init__(self,df):
              self.data = df

       def get_state(self):
              state_info = self.data['Origin_State'][self.data[self.data['Origin_Airport']==self.airport].index]
              for item in state_info:
                     if item is not None:
                            return item 
       def fillstate(self,airport):
              self.airport = airport
              self.data['Origin_State'].fillna(self.get_state(),inplace=True)
              return self.data


fill_none = Autofill(train_data_copy)

for i in tqdm(range(len(train_data_copy['Origin_Airport'].value_counts().index))):
       fill_none.fillstate(train_data_copy['Origin_Airport'].value_counts().index[i])

print(train_data_copy[['Origin_Airport','Origin_State']])
print(train_data_copy.isna().sum())





# 지연되지 않은 항공편 정보만 추출
train_not_delayed = train_data_copy.loc[train_data_copy['Delay_Not_Delayed']==1,['index', 'ID', 'Month', 'Day_of_Month', 'Estimated_Departure_Time',
       'Estimated_Arrival_Time', 'Cancelled', 'Diverted', 'Origin_Airport',
       'Origin_Airport_ID', 'Origin_State', 'Destination_Airport',
       'Destination_Airport_ID', 'Destination_State', 'Distance', 'Airline',
       'Carrier_Code(IATA)', 'Carrier_ID(DOT)', 'Tail_Number', 'Delay_Delayed',
       'Delay_Not_Delayed']]


# print(train_not_delayed.isna().sum())
# print(train_not_delayed.duplicated(subset = ['Distance','Origin_Airport','Destination_Airport','Airline','Carrier_Code(IATA)']).sum())

# print(train_not_delayed.duplicated(subset=['Estimated_Departure_Time','Distance','Origin_Airport','Destination_Airport']).sum())

