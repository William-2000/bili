from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
import pandas as pd
import jieba
import os
#读取训练以及测试数据
os.chdir(r'C:\Users\William\Desktop\bili\data processing')
training_data = pd.read_csv('training_data.csv')
testing_data = pd.read_csv('testing_data.csv')

#划分数据集x_train, x_test, y_train, y_test
x_train = training_data.text
y_train = training_data.emotion
x_test = testing_data.text
y_test = testing_data.emotion
print('x_test', type(x_test))

#特征工程：文本特征抽取-tfidf
transfer = CountVectorizer()
x_train = transfer.fit_transform(x_train)
x_test = transfer.transform(x_test)

#朴素贝叶斯算法预估器流程
estimator = MultinomialNB()
estimator.fit(x_train, y_train)
joblib.dump(estimator, 'estimator.pkl')

if __name__ == "__main__":
    # 模型评估
    # 方法1：直接比对真实值和预测值
    estimator = joblib.load('estimator.pkl')
    y_predict = estimator.predict(x_test)
    print("y_predict:\n", y_predict)
    print("直接比对真实值和预测值:\n", y_test == y_predict)

    # 方法2：计算准确率
    score = estimator.score(x_test, y_test)
    print("准确率为：\n", score)
