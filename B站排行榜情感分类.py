import os
from videodata import VideoData
import bilibilidata
import jieba
import pandas as pd
import joblib
from sklearn.feature_extraction.text import CountVectorizer


# 用于弹幕分词
def cutWords(text):
    return ' '.join(jieba.cut(text))


# 获取B站排行榜数据
os.chdir(r'C:\Users\William\Desktop\bili\bilibili_data')
rank_data = pd.read_csv('all.csv')
rank_url = rank_data.url
rank_title = rank_data.title

url_head = r'https:'
for i in range(len(rank_url)):
    rank_url[i] = url_head + rank_url[i]

# 爬取排行榜每一个视频的基本信息与弹幕
# i = 0
# for each in rank_url:
#     try:
#         os.chdir(r'C:\Users\William\Desktop\bili')
#         video = VideoData(each)
#         video.getDanmaku()
#         i += 1
#         print(i)
#     except:
#         pass

main_sentiment = list()

# 分析排行榜中每一个视频的弹幕情感
os.chdir(r'C:\Users\William\Desktop\bili')
training_data = pd.read_csv('training_data.csv')
x_train = training_data.text
transfer = CountVectorizer()
x_train = transfer.fit_transform(x_train)
estimator = joblib.load('estimator.pkl')

sentiment_tags = dict()
sentiment_tags[0] = 'like'
sentiment_tags[1] = 'sadness'
sentiment_tags[2] = 'disgust'
sentiment_tags[3] = 'anger'
sentiment_tags[4] = 'happiness'

video_num = 1
for each in rank_title:
    print('正在分析第{}个视频'.format(video_num))
    # 打开弹幕文件
    try:
        os.chdir(r'C:\Users\William\Desktop\bili\videos_data\{}'.format(each))
        with open('danmaku.txt', encoding='utf-8') as file:
            danmaku = file.readlines()
    except Exception as exc:
        print(exc)
        print('无法获取弹幕')
    print('成功获取弹幕')

    # 对弹幕与评论分词并转换为Series对象
    for i in range(len(danmaku)):
        danmaku[i] = danmaku[i].replace('\n', '')
    series = pd.Series(danmaku)
    series = series.apply(cutWords)
    print('成功对弹幕分词')

    x_danmaku = transfer.transform(series)
    y_predict = estimator.predict(x_danmaku)

    result = list()
    result.append(list(y_predict).count(1))
    result.append(list(y_predict).count(2))
    result.append(list(y_predict).count(3))
    result.append(list(y_predict).count(4))
    result.append(list(y_predict).count(5))

    video_sentiment = sentiment_tags[result.index(max(result))]
    print('视频{}弹幕的主要情感为{}'.format(video_num, video_sentiment))
    main_sentiment.append(video_sentiment)

    video_num += 1

main_sentiment.count('happiness')