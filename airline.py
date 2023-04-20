import pandas as pd
data = pd.read_csv('C:\\Users\\Playdata\\Desktop\\open\\train.csv')

# Delay 결측치 행 삭제
data = data.dropna(subset=['Delay'], axis=0)

# Airline와 Carrier_ID가 1:1로 대응
# col1을 참고하여 col2의 null 값을 채우는 함수
def airline_fillna(col1, col2):
    dt_array = data[col1].dropna().unique()
    for i in dt_array:
        id = data[data[col1]==i][col2].dropna().unique()[0]
        data.loc[data[col1]==i, col2] = data[data[col1]==i][col2].fillna(id)

# 함수 실행 # Airline와 Carrier_ID가 모두 결측치인 2,985행은 null
airline_fillna('Airline', 'Carrier_ID(DOT)')

# 1:1로 대응되는 Carrier_Code와 Carrier_ID 데이터를 이용하여 결측값 채우기-> 2,185행으로 결측값 줄어듦
for i in ['WN', 'NK', 'B6', 'F9', 'G4', 'VX']:
    id = data[data['Carrier_Code(IATA)']==i]['Carrier_ID(DOT)'].dropna().unique()[0]
    data.loc[data['Carrier_Code(IATA)']==i, 'Carrier_ID(DOT)'] = data[data['Carrier_Code(IATA)']==i]['Carrier_ID(DOT)'].fillna(id)


