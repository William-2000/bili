from sklearn.externals import joblib
import pandas as pd
import jieba
from sklearn.feature_extraction.text import CountVectorizer

estimator = joblib.load('estimator.pkl')
training_data = pd.read_csv('training_data.csv')
x_train = training_data.text


def cutWords(text):
    return ' '.join(jieba.cut(text))


danmaku_file = 'danmaku.txt'
with open(danmaku_file, encoding='utf-8') as file:
    danmaku = file.readlines()

for i in range(len(danmaku)):
    danmaku[i] = danmaku[i].replace('\n', '')

series = pd.Series(danmaku)
series = series.apply(cutWords)
print(series)

transfer = CountVectorizer()
x_train = transfer.fit_transform(x_train)
x_danmaku = transfer.transform(series)
print(x_danmaku)

y_predict = estimator.predict(x_danmaku)
result = list(y_predict)
print('0', result.count(0))
print('1', result.count(1))
print('2', result.count(2))
print('3', result.count(3))
print('4', result.count(4))
print('5', result.count(5))
print('6', result.count(6))
print('7', result.count(7))