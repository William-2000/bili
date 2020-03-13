import os
import pandas as pd
from snownlp import SnowNLP
import bilibilidata
from videodata import VideoData
import matplotlib.pyplot as plt
import matplotlib as mpl
import jieba
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import characterart
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
print('已成功导入所需的包')

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.family'] = 'sans-serif'
font_path = r'C:\Windows\Fonts\新蒂剪纸体.ttf'


# 爬虫
# a) 爬取指定视频的基本信息（包括视频标题，视频类别，弹幕数量，评论数量）
def getVideoInfo_demo():
    video_url = 'https://www.bilibili.com/video/av68733672'
    video1 = VideoData(video_url)


# b) 视频的所有评论
def getVideoComment_demo():
    video_url = 'https://www.bilibili.com/bangumi/play/ep285946'
    video2 = VideoData(video_url)
    video2.getVideoComment()


# c) 视频的所有弹幕
def getDanmaku_demo():
    video_url = 'https://www.bilibili.com/video/av78273046'
    video3 = VideoData(video_url)
    video3.getDanmaku()


# d) B站排行榜
def getRank_demo():
    os.chdir(r"bilibili_data")
    # 获取排行
    bilibilidata.getRank()
    # 获取动漫排行
    bilibilidata.getRank(rank_type="bangumi")
    # 获取影视类别排行
    bilibilidata.getRank(rank_type="cinema")


# 数据分析
# a) 某个指定视频的评论与弹幕情感极性分析
def EmotionalPolarity_demo():
    # video_url = 'https://www.bilibili.com/video/av76394931'
    # video = VideoData(video_url)
    # video.getDanmaku()
    # video.getVideoComment()
    # video_title = video.video_info['title']
    # video_path = 'C:\\Users\\William\\Desktop\\bili\\videos_data\\{}'.format(
    #     video_title)
    video_path = 'C:\\Users\\William\\Desktop\\bili\\videos_data\\【香港真相大起底】暴力乱港实录'
    os.chdir(video_path)
    with open('danmaku.txt', encoding='utf-8') as file:
        danmaku = file.readlines()
    with open('replies.txt', encoding='utf-8') as file:
        replies = file.readlines()
    print('成功读取弹幕与评论')

    # 从指定视频文件夹下获取文件并进行极性分析
    print('正在进行极性分析')
    danmaku_sentiments = list()
    for i in range(len(danmaku)):
        s = SnowNLP(danmaku[i])
        danmaku_sentiments.append(s.sentiments)
    replies_sentiments = list()
    for i in range(len(replies)):
        s = SnowNLP(replies[i])
        replies_sentiments.append(s.sentiments)

    # 将分析结果分为积极、消极、中性
    danmaku_positive_num = 0
    danmaku_negative_num = 0
    danmaku_nuetral_num = 0
    for each in danmaku_sentiments:
        if each > 0.5:
            danmaku_positive_num += 1
        if each < 0.5:
            danmaku_negative_num += 1
        if each == 0.5:
            danmaku_nuetral_num += 1
    replies_positive_num = 0
    replies_negative_num = 0
    replies_nuetral_num = 0
    for each in replies_sentiments:
        if each > 0.5:
            replies_positive_num += 1
        if each < 0.5:
            replies_negative_num += 1
        if each == 0.5:
            replies_nuetral_num += 1

    # 将分析结果可视化
    labels = ['积极', '消极', '中性']
    danmaku_share = [
        danmaku_positive_num, danmaku_negative_num, danmaku_nuetral_num
    ]
    replies_share = [
        replies_positive_num, replies_negative_num, replies_nuetral_num
    ]

    pie_danmaku_data = [list(each) for each in zip(labels, danmaku_share)]
    pie_replies_data = [list(each) for each in zip(labels, replies_share)]

    # 弹幕部分
    print('正在生成弹幕部分的图')
    pie_danmaku = Pie(init_opts=opts.InitOpts(
        width='960px', height='540px', theme=ThemeType.WHITE))

    pie_danmaku.add(
        '弹幕情感极性分析',
        pie_danmaku_data,
        radius=['50%', '80%'],
    )

    pie_danmaku.set_global_opts(
        title_opts=opts.TitleOpts(
            '弹幕情感极性分析',
            subtitle='情感比例图',
            title_textstyle_opts=opts.TextStyleOpts(font_size=30),
            subtitle_textstyle_opts=opts.TextStyleOpts(font_size=25)),
        legend_opts=opts.LegendOpts(
            pos_left='90%',
            pos_top='20%',
            orient='vertical',
            textstyle_opts=opts.TextStyleOpts(font_size=20)))
    pie_danmaku.set_series_opts(
        label_opts=opts.LabelOpts(formatter='{b}: {d}%', font_size=20))

    os.chdir(video_path)
    pie_danmaku.render('弹幕情感极性分析.html')
    make_snapshot(snapshot, pie_danmaku.render(), '弹幕情感极性分析.png')

    # 评论部分
    print('正在生成评论部分的图')
    pie_replies = Pie(init_opts=opts.InitOpts(
        width='960px', height='540px', theme=ThemeType.WHITE))

    pie_replies.add(
        '评论情感极性分析',
        pie_replies_data,
        radius=['50%', '80%'],
    )

    pie_replies.set_global_opts(
        title_opts=opts.TitleOpts(
            '评论情感极性分析',
            subtitle='情感比例图',
            title_textstyle_opts=opts.TextStyleOpts(font_size=30),
            subtitle_textstyle_opts=opts.TextStyleOpts(font_size=25)),
        legend_opts=opts.LegendOpts(
            pos_left='90%',
            pos_top='20%',
            orient='vertical',
            textstyle_opts=opts.TextStyleOpts(font_size=20)))
    pie_replies.set_series_opts(
        label_opts=opts.LabelOpts(formatter='{b}: {d}%', font_size=20))

    pie_replies.render('评论情感极性分析.html')
    make_snapshot(snapshot, pie_replies.render(), '评论情感极性分析.png')

    # 数量图
    bar = Bar(init_opts=opts.InitOpts(
        width='960px', height='540px', theme=ThemeType.WALDEN))

    bar.add_xaxis(labels)
    bar.add_yaxis('弹幕', danmaku_share, category_gap='60%')
    bar.add_yaxis('评论', replies_share, category_gap='60%')

    bar.set_global_opts(title_opts=opts.TitleOpts(
        title='情感极性分析',
        subtitle='数量图',
        title_textstyle_opts=opts.TextStyleOpts(font_size=30),
        subtitle_textstyle_opts=opts.TextStyleOpts(font_size=20)),
                        legend_opts=opts.LegendOpts(
                            textstyle_opts=opts.TextStyleOpts(font_size=20)))

    bar.set_series_opts(
        itemstyle_opts={"normal": {
            "barBorderRadius": [30, 30, 30, 30]
        }},
        label_opts=opts.LabelOpts(font_size=20))

    bar.render('情感极性分析数量图.html')
    make_snapshot(snapshot, bar.render(), '情感极性分析数量图.png')


# b) 某个指定视频的评论与弹幕情感分类
def sentimentClassification_demo():
    # 爬取指定视频信息
    # video_url = 'https://www.bilibili.com/video/av68733672'
    # video = VideoData(video_url)
    # video.getDanmaku()
    # video.getVideoComment()
    # video_title = video.video_info['title']
    video_title = '【藏】南京大屠杀死难者国家公祭日【风鸣社】'
    danmaku_path = 'C:\\Users\\William\\Desktop\\bili\\videos_data\\{}\\danmaku.txt'.format(
        video_title)
    replies_path = 'C:\\Users\\William\\Desktop\\bili\\videos_data\\{}\\replies.txt'.format(
        video_title)

    def cutWords(text):
        return ' '.join(jieba.cut(text))

    # 读取视频的弹幕与评论文件
    try:
        with open(danmaku_path, encoding='utf-8') as file:
            danmaku = file.readlines()
        with open(replies_path, encoding='utf-8') as file:
            replies = file.readlines()
    except:
        print('无法获取弹幕或评论')
        return
    print("成功获取弹幕与评论")

    # 对弹幕与评论分词并转换为Series对象
    for i in range(len(danmaku)):
        danmaku[i] = danmaku[i].replace('\n', '')
    series1 = pd.Series(danmaku)
    series1 = series1.apply(cutWords)
    for i in range(len(replies)):
        replies[i] = replies[i].replace('\n', '')
    series2 = pd.Series(replies)
    series2 = series2.apply(cutWords)

    # 将弹幕转换为词向量
    os.chdir(r'C:\Users\William\Desktop\bili')
    training_data = pd.read_csv('training_data.csv')
    x_train = training_data.text
    transfer = CountVectorizer()
    x_train = transfer.fit_transform(x_train)
    x_danmaku = transfer.transform(series1)
    x_replies = transfer.transform(series2)
    estimator = joblib.load('estimator.pkl')
    y_predict1 = estimator.predict(x_danmaku)
    y_predict2 = estimator.predict(x_replies)

    # 生成弹幕情感分类
    sentiments = ['none', 'like', 'sadness', 'disgust', 'anger', 'happiness']
    sentiments_data = [list(y_predict1).count(i) for i in range(6)]

    pie_data = [list(each) for each in zip(sentiments, sentiments_data)]
    pie = Pie(init_opts=opts.InitOpts(
        width='960px', height='540px', theme=ThemeType.WALDEN))
    pie.add('弹幕情绪分类', pie_data, radius=['30%', '75%'], rosetype='radius')

    pie.set_global_opts(title_opts=opts.TitleOpts(
        '弹幕情绪分类',
        subtitle='情绪比例图',
        title_textstyle_opts=opts.TextStyleOpts(font_size=30),
        subtitle_textstyle_opts=opts.TextStyleOpts(font_size=25)),
                        legend_opts=opts.LegendOpts(
                            pos_left='90%',
                            pos_top='20%',
                            orient='vertical',
                            textstyle_opts=opts.TextStyleOpts(font_size=20)))
    pie.set_series_opts(
        label_opts=opts.LabelOpts(formatter='{b}: {d}%', font_size=20))

    os.chdir(
        r'C:\Users\William\Desktop\bili\videos_data\{}'.format(video_title))
    pie.render('弹幕情绪分类.html')
    make_snapshot(snapshot, pie.render(), '弹幕情绪分类.png')

    # 生成评论情感分类
    sentiments = ['like', 'sadness', 'disgust', 'anger', 'happiness']
    sentiments_data = [list(y_predict2).count(i) for i in range(1, 6)]

    pie_data = [list(each) for each in zip(sentiments, sentiments_data)]
    pie = Pie(init_opts=opts.InitOpts(
        width='960px', height='540px', theme=ThemeType.WALDEN))
    pie.add('评论情绪分类', pie_data, radius=['30%', '75%'], rosetype='radius')

    pie.set_global_opts(title_opts=opts.TitleOpts(
        '评论情绪分类',
        subtitle='情绪比例图',
        title_textstyle_opts=opts.TextStyleOpts(font_size=30),
        subtitle_textstyle_opts=opts.TextStyleOpts(font_size=25)),
                        legend_opts=opts.LegendOpts(
                            pos_left='90%',
                            pos_top='20%',
                            orient='vertical',
                            textstyle_opts=opts.TextStyleOpts(font_size=20)))
    pie.set_series_opts(
        label_opts=opts.LabelOpts(formatter='{b}: {d}%', font_size=20))

    os.chdir(
        r'C:\Users\William\Desktop\bili\videos_data\{}'.format(video_title))
    pie.render('评论情绪分类.html')
    make_snapshot(snapshot, pie.render(), '评论情绪分类.png')


# c) 某个指定视频的弹幕词云
def danmakuWordcloud_demo():
    # 爬取指定视频信息
    # video_url = 'https://www.bilibili.com/video/av79122654'
    # video = VideoData(video_url)
    # video.getDanmaku()
    # video.getVideoComment()
    # video_title = video.video_info['title']
    video_title = '【藏】南京大屠杀死难者国家公祭日【风鸣社】'
    danmaku_path = 'C:\\Users\\William\\Desktop\\bili\\videos_data\\{}\\danmaku.txt'.format(
        video_title)
    try:
        with open(danmaku_path, encoding='utf-8') as file:
            danmaku = file.readlines()
    except:
        print('获取弹幕失败')
        # return
    print('成功获取弹幕')

    # 加载停用词
    path = 'C:\\Users\\William\\Desktop\\bili\\百度停用词表.txt'
    with open(path, encoding='utf-8') as file:
        file_content = file.readlines()
    stopwords = set()
    for i in range(len(file_content)):
        file_content[i] = file_content[i].replace("\n", "")
        stopwords.add(file_content[i])

    wordcloud_text = str()
    for each in danmaku:
        each = each.replace('\n', '')
        each += ' '
        wordcloud_text += each

    wc1 = WordCloud(
        background_color='white',
        font_path=font_path,
        width=900,
        height=450,
        scale=3,
        max_font_size=70,
        # min_font_size=10,
        max_words=400,
        stopwords=stopwords)
    print('开始生成词云')
    wc1.generate(wordcloud_text)

    plt.imshow(wc1, interpolation='bilinear')
    plt.axis('off')
    os.chdir('C:\\Users\\William\\Desktop\\bili\\videos_data\\{}'.format(
        video_title))
    plt.savefig('./弹幕词云.png')


# d) B站排行榜视频的评论与弹幕情感分类
def bilibiliSentimentClassification_demo():
    # 用于弹幕分词
    def cutWords(text):
        return ' '.join(jieba.cut(text))

    # 获取B站排行榜数据
    bilibilidata.getRank()
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
            os.chdir(
                r'C:\Users\William\Desktop\bili\videos_data\{}'.format(each))
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

    sentiments = ['none', 'like', 'sadness', 'disgust', 'anger', 'happiness']
    sentiments_data = [main_sentiment.count(each) for each in sentiments]

    pie_data = [list(each) for each in zip(sentiments, sentiments_data)]
    pie = Pie(init_opts=opts.InitOpts(
        width='960px', height='540px', theme=ThemeType.WALDEN))
    pie.add('排行榜情绪分类',
            pie_data,
            radius=['30%', '75%'],
            rosetype='radius',
            label_opts=opts.LabelOpts(
                position='outside',
                formatter='{a|{a}}{abg|}\n{hr|}\n{b|{b}: }{c}   {per|{d}%}  ',
                background_color='#eee',
                border_color='#aaa',
                border_width=1,
                border_radius=4,
                rich={
                    'a': {
                        'color': '#999',
                        'lineHeight': 22,
                        'align': 'center'
                    },
                    'abg': {
                        'bakgroundColor': '#e3e3e3',
                        'width': '100%',
                        'align': 'right',
                        'height': 22,
                        'borderRadius': [4, 4, 0, 0]
                    },
                    'hr': {
                        'borderColor': '#aaa',
                        'width': '100%',
                        'borderWidth': 0.5,
                        'height': 0
                    },
                    'b': {
                        'fontSize': 16,
                        'lineHeight': 33
                    },
                    'per': {
                        'color': '#eee',
                        'backgroundColor': '#334455',
                        'padding': [2, 4],
                        'borderRadius': 2
                    }
                }))
    pie.set_global_opts(title_opts=opts.TitleOpts(title='排行榜情绪分类'))

    os.chdir(r'C:\Users\William\Desktop\bili')
    pie.render('排行榜情绪分类.html')
    make_snapshot(snapshot, pie.render(), '排行榜情绪分类.png')


# e) B站排行榜数量分布图
def bilibiliData_demo():
    # 获取B站排行榜数据
    bilibilidata.getRank()
    os.chdir(r'C:\Users\William\Desktop\bili\bilibili_data')
    rank_data = pd.read_csv('all.csv')
    print('成功获取排行榜数据')
    rank_url = rank_data.url
    rank_title = rank_data.title

    url_head = r'https:'
    for i in range(len(rank_url)):
        rank_url[i] = url_head + rank_url[i]

    # 爬取排行榜每一个视频的基本信息
    # print('正在爬取排行榜每一个视频的基本信息')
    # process_num = 1
    # for each in rank_url:
    #     try:
    #         os.chdir(r'C:\Users\William\Desktop\bili')
    #         video = VideoData(each)
    #         print(i)
    #         i += 1
    #     except:
    #         i+=1

    danmaku_list = list()
    replies_list = list()
    favorite_list = list()
    coin_list = list()
    like_list = list()

    for each in rank_title:
        each_video_info = list()
        try:
            os.chdir(
                r'C:\Users\William\Desktop\bili\videos_data\{}'.format(each))
            info = pd.read_csv('video_info.csv')
        except Exception as exc:
            print('无法打开文件')
            continue
        print('成功获取文件')

        info = pd.DataFrame(info.values.T)
        danmaku_list.append(int(info[5][1])) # 弹幕
        replies_list.append(int(info[6][1]))  # 评论
        favorite_list.append(int(info[7][1]))  # 收藏
        coin_list.append(int(info[8][1]))  # 投币
        like_list.append(int(info[9][1]))  # 喜爱

    x_axis = list(range(100, 0, -1))
    bar = Bar(init_opts=opts.InitOpts(
    width='1600px', height='900px', theme=ThemeType.WALDEN))

    bar.add_xaxis(x_axis)
    bar.add_yaxis('弹幕', danmaku_list)
    bar.add_yaxis('评论', replies_list, is_selected=False)
    bar.add_yaxis('收藏', favorite_list, is_selected=False)
    bar.add_yaxis('投币', coin_list, is_selected=False)
    bar.add_yaxis('喜爱', like_list, is_selected=False)
    bar.reversal_axis()

    bar.set_global_opts(datazoom_opts=opts.DataZoomOpts(orient='vertical'))

    os.chdir(r'C:\Users\William\Desktop\bili')
    bar.render('排行榜数量分布图.html')
    make_snapshot(snapshot, bar.render(), '排行榜数量分布图.png')

# f) 排行榜最热门视频类别词云
def tagsWordcloud_demo():
    bilibilidata.getRank()
    os.chdir(r'C:\Users\William\Desktop\bili\bilibili_data')
    rank_data = pd.read_csv('all.csv')
    print('成功获取排行榜数据')
    rank_url = rank_data.url
    rank_title = rank_data.title

    url_head = r'https:'
    for i in range(len(rank_url)):
        rank_url[i] = url_head + rank_url[i]

    # 爬取排行榜每一个视频的基本信息
    print('正在爬取排行榜每一个视频的基本信息')
    process_num = 1
    for each in rank_url:
        try:
            os.chdir(r'C:\Users\William\Desktop\bili')
            video = VideoData(each)
            video.getVideoTags()
            print(process_num)
            process_num += 1
        except:
            process_num += 1

    # 读取每一个视频的标签
    tags = list()
    os.chdir(r'C:\Users\William\Desktop\bili')
    for each in rank_title:
        try:
            os.chdir(
                r'C:\Users\William\Desktop\bili\videos_data\{}'.format(each))
            with open('tags.txt', encoding='utf-8') as file:
                tags.append(file.readlines())
        except Exception as exc:
            pass

    tags_txt = str()
    for each_video_tags in tags:
        for each_tag in each_video_tags:
            tags_txt += each_tag

    tags_txt = tags_txt.replace('\n', ' ')

    # 加载停用词
    path = 'C:\\Users\\William\\Desktop\\bili\\百度停用词表.txt'
    with open(path, encoding='utf-8') as file:
        file_content = file.readlines()
    stopwords = set()
    for i in range(len(file_content)):
        file_content[i] = file_content[i].replace("\n", "")
        stopwords.add(file_content[i])

    # 生成视频标签词云
    wc = WordCloud(background_color='white',
                   font_path=font_path,
                   stopwords=stopwords,
                   width=1920,
                   height=1080,
                   scale=2)
    wc.generate(tags_txt)
    plt.imshow(wc)
    plt.axis('off')
    os.chdir('C:\\Users\\William\\Desktop\\bili')
    plt.savefig('./排行榜标签词云.png')


# g) B站热门弹幕词云


# 字符画
def characterArt_demo():
    video_url = 'https://www.bilibili.com/video/av79839682'
    video = VideoData(video_url)
    print('正在获取弹幕')
    video.getDanmaku()
    print('正在获取评论')
    video.getVideoComment()
    video_title = video.video_info['title']
    # video_title = '「鬼灭之刃」温柔到让人哭泣的心——心碎者的柔歌'
    video_path = 'C:\\Users\\William\\Desktop\\bili\\videos_data\\{}'.format(
        video_title)
    os.chdir(video_path)
    img_file = 'cover.jpg'
    danmaku_file = 'danmaku.txt'
    replies_file = 'replies.txt'
    print('正在生成字符画')

    characterart.createCharacterArt(img_file, danmaku_file, replies_file)
    print('已成功保存字符画')


if __name__ == "__main__":
    bilibiliData_demo()
