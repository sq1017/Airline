from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PATH = '/home/park/다운로드/titanic/train.csv'
data = pd.read_csv(PATH)

data.drop(columns=['Cabin','Name','Ticket'],inplace=True)
data.head()

data.dropna(subset=['Embarked'],axis=0,inplace=True)
data.fillna(data['Age'].mean(),inplace=True)

data = pd.get_dummies(data,columns=['Embarked','Sex'])

y = data.pop('Survived')
stscaler = StandardScaler()
data_scaled = stscaler.fit_transform(data)


data_scaled = pd.DataFrame(data_scaled,columns=data.columns)

X = data_scaled
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,stratify=y)

model = DecisionTreeClassifier()
model.fit(X_train,y_train)
y_pred = model.predict(X_test)

model_ran = RandomForestClassifier()
model_ran.fit(X_train,y_train)
y_pred_ran = model_ran.predict(X_test)



## 여기서부터 파이 차트
## wedgeprops : 중간 비워서 도넛 형태로 만든 요소
## autopct : 백분율 표시 추가
## labeldistance : 레이블을 차트 안쪽에 넣기 가능(2번 차트에 사용)
## 중요사항 추가 : seaborn 라이브러리에서 sns.color_palette 를 사용하면 칼라 세트 사용 가능(2번 차트에 사용)

fig = plt.figure(figsize=[10,8])
plt.subplot(1,2,1)
plt.pie(model.feature_importances_,labels=data_scaled.columns,wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 1},colors=['#A0DB8E','#FAD6A5','#FF7F50','#FFFB96','#B967FF','#FFC2CD','#FF7F50','#DAF8E3','#005582','#00C2C7','#FFF9AE'],shadow=True,autopct='%.2f%%')
plt.subplot(1,2,2)


plt.pie(model_ran.feature_importances_,colors=sns.color_palette('Set2'),labeldistance=0.75,labels=data_scaled.columns,shadow=True,wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 1})

plt.show()
