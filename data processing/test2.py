from sklearn.externals import joblib
import pandas as pd
import jieba
from sklearn.feature_extraction.text import CountVectorizer

estimator = joblib.load('estimator.pkl')
training_data = pd.read_csv('training_data.csv')
testing_data = pd.read_csv('testing_data.csv')
with open('danmaku.txt', encoding='utf-8') as file:
    danmaku = file.readlines()

x_test = testing_data.text
x_train = training_data.text

print(x_test)

transfer = CountVectorizer()
x_train = transfer.fit_transform(x_train)
x_test = transfer.transform(x_test)
y_predict = estimator.predict(x_test)
print(y_predict)