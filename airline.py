import pandas as pd
from sklearn.preprocessing import LabelEncoder


# 항공사 코드 결측치 처리


# data = pd.read_csv('./open/train.csv')
data=pd.read_csv('./2.csv')

# Delay 결측치 행 삭제 후 인코딩
data = data.dropna(subset=['Delay'], axis=0).reset_index(drop=True)
data = pd.get_dummies(data,columns=['Delay'])

# bool형인 종속변수는 int형으로
data['Delay_Delayed'] = data['Delay_Delayed'].astype(int)
data['Delay_Not_Delayed'] = data['Delay_Not_Delayed'].astype(int)

# state 결측치 제거
class Autofill():
       def __init__(self,df):
              self.data = df

       def get_ori_state(self):
              state_info = self.data['Origin_State'][self.data[self.data['Origin_Airport']==self.airport].index]
              for item in state_info:
                     if item is not None:
                            return item 
       def fill_ori_state(self,airport):
              self.airport = airport
              self.data['Origin_State'].fillna(self.get_ori_state(),inplace=True)
              return self.data
       
       def get_dest_state(self):
              state_info = self.data['Destination_State'][self.data[self.data['Destination_Airport']==self.airport].index]
              for item in state_info:
                     if item is not None:
                            return item 
       def fill_dest_state(self,airport):
              self.airport = airport
              self.data['Destination_State'].fillna(self.get_dest_state(),inplace=True)
              return self.data

fill_none = Autofill(data)

for i in (range(len(data['Origin_Airport'].value_counts().index))):
       fill_none.fill_ori_state(data['Origin_Airport'].value_counts().index[i])
for i in (range(len(data['Destination_Airport'].value_counts().index))):
       fill_none.fill_dest_state(data['Destination_Airport'].value_counts().index[i])

# Airline와 Carrier_ID가 1:1로 대응
# carrier_id 결측치 제거(결측치: 2,985행)
def airline_fillna(col1, col2):
    dt_array = data[col1].dropna().unique()
    for i in dt_array:
        id = data[data[col1]==i][col2].dropna().unique()[0]
        data.loc[data[col1]==i, col2] = data[data[col1]==i][col2].fillna(id)

airline_fillna('Airline', 'Carrier_ID(DOT)')

# 1:1로 대응되는 Carrier_Code와 Carrier_ID 데이터를 이용하여 결측치 추가 제거(결측치: 2,185행)
for i in ['WN', 'NK', 'B6', 'F9', 'G4', 'VX']:
    id = data[data['Carrier_Code(IATA)']==i]['Carrier_ID(DOT)'].dropna().unique()[0]
    data.loc[data['Carrier_Code(IATA)']==i, 'Carrier_ID(DOT)'] = data[data['Carrier_Code(IATA)']==i]['Carrier_ID(DOT)'].fillna(id)

# carrier_id 결측치(2,185행) 삭제
data = data.dropna(subset=['Carrier_ID(DOT)'], axis=0).reset_index(drop=True)

# origin_state / destination_state / tail_number 인코딩
le = LabelEncoder()
data_tail = le.fit_transform(data['Tail_Number'])
data_or = le.fit_transform(data['Origin_State'])
data_de = le.fit_transform(data['Destination_State'])
data_le = pd.DataFrame({'tail_num': data_tail, 'origin_st':data_or, 'destination_st':data_de})

data = pd.concat([data, data_le], axis=1)

# 필요 없는 컬럼 삭제
data.drop(['Airline', 'Carrier_Code(IATA)'], axis=1, inplace=True)
data.drop(['Cancelled', 'Diverted', 'Origin_Airport', 'Destination_Airport', 'Delay_Not_Delayed'], axis=1, inplace=True)
data.drop(['ID', 'Origin_State', 'Destination_State'], axis=1, inplace=True)

# data.to_csv('airline_code_complete.csv')
data.to_csv('3.csv')

