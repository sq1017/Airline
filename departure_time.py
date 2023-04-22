import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# OPEN file : train.csv
airline_ori=pd.read_csv('./open/train.csv')

# extract data of time and distance
target_data=['Estimated_Departure_Time','Estimated_Arrival_Time','Distance']
time_distance=airline_ori[target_data]
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
airline_ori.loc[departure_data_bak.index, 'Estimated_Departure_Time']=departure_data_bak['Estimated_Departure_Time']

print('THE END :3')