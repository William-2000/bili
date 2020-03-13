from xml.dom.minidom import parse
import xml.dom.minidom
import pandas as pd
import os
import json
import jieba


# 用于解析xml类型的training数据
def parseTrainingData1(file_name, target_name):
    text = list()
    emotion = list()

    DOMTree = xml.dom.minidom.parse(file_name)
    TrainData = DOMTree.documentElement
    sentences = TrainData.getElementsByTagName('sentence')
    for each_sentence in sentences:
        text.append(each_sentence.childNodes[0].data)
        opinionated = each_sentence.getAttribute('opinionated')
        if opinionated == 'Y':
            emotion_type = each_sentence.getAttribute('emotion-1-type')
            if emotion_type == 'like':
                emotion.append(1)
            if emotion_type == 'sadness':
                emotion.append(2)
            if emotion_type == 'disgust':
                emotion.append(3)
            if emotion_type == 'anger':
                emotion.append(4)
            if emotion_type == 'happiness':
                emotion.append(5)
            if emotion_type == 'surprise':
                emotion.append(6)
            if emotion_type == 'fear':
                emotion.append(7)
        else:
            emotion.append(0)

    emotion_data = dict()
    emotion_data['text'] = text
    emotion_data['emotion'] = emotion

    df = pd.DataFrame(emotion_data)
    df.to_csv('{}.csv'.format(target_name), encoding='utf-8')


# 用于解析train.json
def parseTrainingData2(file_name, target_name):
    with open(file_name, encoding='utf-8') as file:
        file_content = file.readlines()

    content = str()
    for each in file_content:
        content += each

    content.replace('\n', '')

    json_content = json.loads(content)
    text = list()
    emotion = list()

    for each in json_content:
        each[0] = each[0].replace('\n', '')
        text.append(each[0])
        emotion.append(each[1])

    emotion_data = dict()
    emotion_data['text'] = text
    emotion_data['emotion'] = emotion

    df = pd.DataFrame(emotion_data)
    df.to_csv('{}.csv'.format(target_name), encoding='utf-8')


# 用于解析xml类型的training数据
# if __name__ == "__main__":
#     file1 = 'Training data for Emotion Classification.xml'
#     target_name1 = 'training_data1'
#     parseTrainingData1(file1, target_name1)

#     file2 = 'Training data for Emotion Expression Identification.xml'
#     target_name2 = 'testing_data1'
#     parseTrainingData1(file2, target_name2)

# 用于解析train.json
# if __name__ == "__main__":
#     # file_dir = 'D:\Python\解析数据'
#     file_name = 'train.json'
#     target_name = 'training_data2'
#     parseTrainingData2(file_name, target_name)


# 将testing_data1 与 training_data1中的text字段中的数据进行分词
def cutWords(text):
    return ' '.join(jieba.cut(text))


file_name1 = 'testing_data1.csv'
file_name2 = 'training_data1.csv'
file_name3 = 'test2.csv'

testing_data1 = pd.read_csv(r'data2\{}'.format(file_name3), index_col='index')
testing_data1['text'] = testing_data1['text'].apply(cutWords)
testing_data1.to_csv(r'data2\{}'.format(file_name3))
