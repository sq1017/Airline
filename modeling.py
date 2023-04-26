import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import log_loss

# data = pd.read_csv('C:\\Users\\Playdata\\Desktop\\playdata\\project\\ML_project\\preprocessed_1.csv')
# data = pd.read_csv('C:\\Users\\Playdata\\Desktop\\playdata\\project\\ML_project\\preprocessed_2.csv')
# data = pd.read_csv('C:\\Users\\Playdata\\Desktop\\playdata\\project\\ML_project\\preprocessed_3.csv')
data = pd.read_csv('C:\\Users\\Playdata\\Desktop\\playdata\\project\\ML_project\\train_del.csv')
# data = pd.read_csv('C:\\Users\\Playdata\\Desktop\\playdata\\project\\ML_project\\final.csv')

# data.drop(['Unnamed: 0.1', 'level_0', 'Unnamed: 0', 'index'], axis=1, inplace=True)
data.drop('Unnamed: 0', axis=1, inplace=True)
data.dropna(inplace=True)

y = data.pop('Delay')
X = data

scaler = MinMaxScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=22)

# rf_model = RandomForestClassifier(max_depth=3)
# lg_model = LogisticRegression()
# knn_model = KNeighborsClassifier(n_neighbors=7)
# tree_model = DecisionTreeClassifier(max_depth=3)
lgb_model = LGBMClassifier(max_depth=2)

# rf_model.fit(X_train, y_train)
# lg_model.fit(X_train, y_train)
# knn_model.fit(X_train, y_train)
# tree_model.fit(X_train, y_train)
lgb_model.fit(X_train, y_train)

# rf_pred = rf_model.predict(X_test)
# lg_pred = lg_model.predict(X_test)
# knn_pred = knn_model.predict(X_test)
# tree_pred = tree_model.predict(X_test)
# lgb_pred = lgb_model.predict(X_test)

# print('Random Forest:', log_loss(y_test, rf_pred))
# print('Logistic:', log_loss(y_test, lg_pred))
# print('KNN:', log_loss(y_test, knn_pred))
# print('Decision Tree:', log_loss(y_test, tree_pred))
# print('LGBM:', log_loss(y_test, lgb_pred))

test = pd.read_csv('C:\\Users\\Playdata\\Desktop\\playdata\\project\\ML_project\\test2.csv')
test.drop('Unnamed: 0', axis=1, inplace=True)

pred_test = lgb_model.predict(test)

submission = pd.read_csv('C:\\Users\\Playdata\\Desktop\\playdata\\project\\ML_project\\open\\sample_submission.csv')

submission['Delayed'] = pred_test
submission['Not_Delayed'] = 1

submission.to_csv('sub.csv', index=False)