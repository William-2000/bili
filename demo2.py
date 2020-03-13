from videodata import VideoData

video_url = 'https://www.bilibili.com/video/av80565276'  # 指定需要爬取的视频url

video = VideoData(video_url)  # 初始化视频对象，生成对应的文件夹并获取基本信息与封面
video.getDanmaku()  # 获取视频的弹幕
video.getVideoComment()  # 获取视频的评论
video.getVideoTags()  # 获取视频标签

video.getVideoData()  # 获取弹幕评论和标签

import bilibilidata

# getRank(url=None, rank_type='all')
bilibilidata.getRank()  # 默认获取全站排行榜

# 指定rank_type参数：all、origin、bangumi、cinema、rookie
bilibilidata.getRank(rank_type='bangumi')

# 指定排行榜url
rank_url = 'https://www.bilibili.com/ranking/cinema/23/0/3'
bilibilidata.getRank(url=rank_url)