import json
import os
import os.path
import re
import threading
import bs4 as bs
import requests
import pandas as pd


class VideoData:
    __url = ""  # 视频的url
    __html = ""  # 视频url的源代码
    __cid = ""  # 用于获取弹幕
    __aid = ""  # 用于获取评论
    video_info = dict()  # 视频的标题，通过__getVideoInfo()获取

    # 获取一个url的源代码
    @staticmethod
    def getHTMLText(url):
        headers = {
            "User-Agent":
            r"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text
        except:
            return ""

    # 通过一个视频的url确定一个对象，通过解析url页面的源码获取对象的基本信息，并创建相应的文件夹保存当前视频的信息
    def __init__(self, url):
        self.__url = url
        self.__html = VideoData.getHTMLText(url)
        self.__cid = self.__getcid()
        self.__aid = self.__getaid()
        self.video_info = self.__getVideoInfo()

    # 输出__cid, __aid, video_info
    def __repr__(self):
        info = str()
        for each in self.video_info:
            info += "{}:{}\n".format(each, self.video_info[each])
        return info

    # 获取视频基本信息
    def __getVideoInfo(self):
        url = "https://api.bilibili.com/x/web-interface/view?aid={}&cid={}".format(
            self.__aid, self.__cid)
        video_info = dict()
        try:
            html = VideoData.getHTMLText(url)
            if html is "":
                raise Exception("getHTMLError")
            data = json.loads(html)

            if data["code"] is not 0:
                raise Exception("getVideoInfoError")
            data = data["data"]
            video_info["aid"] = self.__aid  # 视频av号
            video_info["cid"] = self.__cid  # cid用于获取弹幕
            video_info[
                "video url"] = "https://www.bilibili.com/video/av{}".format(
                    self.__aid)
            video_info["title"] = data["title"]  # 视频标题
            video_info["tname"] = data["tname"]  # 视频类型
            video_info["owner"] = data["owner"]["name"]  # 作者
            video_info["danmaku"] = data["stat"]["danmaku"]  # 弹幕数
            video_info["reply"] = data["stat"]["reply"]  # 评论数
            video_info["favorite"] = data["stat"]["favorite"]  # 收藏数
            video_info["coin"] = data["stat"]["coin"]  # 投币数
            video_info["like"] = data["stat"]["like"]  # 点赞数
            video_info["pic"] = data["pic"]  # 视频封面

        except Exception as error:
            print("{}".format(error))
            return {}

        info_series = pd.Series(video_info)
        # 将视频信息保存到视频对应文件夹中的video_info.csv
        if os.path.relpath(os.path.abspath("."),
                           os.path.abspath("..")) == "bili":
            if not os.path.exists("videos_data"):
                os.makedirs("videos_data")
            if not os.path.exists("bilibili_data"):
                os.makedirs("bilibili_data")
            if video_info["title"] is not "":
                os.chdir(r"videos_data")
                if not os.path.exists("{}".format(video_info["title"])):
                    os.makedirs("{}".format(video_info["title"]))

        info_series.to_csv("{}/video_info.csv".format(video_info["title"]),
                           header=0,
                           encoding="utf-8")
        # 将视频封面保存到视频对应文件夹
        content = requests.get(video_info["pic"]).content
        with open("{}/cover.jpg".format(video_info["title"]), "wb") as file:
            file.write(content)

        return video_info

    # 获取视频aid号
    def __getaid(self):
        if self.__url.find("av") is not -1:
            span = re.search(r"av[\d]+", self.__url).span()
            aid = self.__url[span[0]:span[1]].replace("av", "")
        else:
            try:
                soup = bs.BeautifulSoup(self.__html, "html.parser")
                aid = soup.find("a", {
                    "class": "aid-link"
                }).text.replace("av", "")
            except:
                aid = ""
        if aid == '':
            try:
                aid = soup.find('a', {
                    'class': 'av-link'
                }).text.replace('AV', '')
            except:
                aid = ''
        return aid

    # 获取视频cid
    def __getcid(self):
        label = [
            "http://upos-hz-mirrorhw.acgvideo.com/upgcxcode/",
            "http://upos-hz-mirrorks3u.acgvideo.com/upgcxcode/",
            "http://upos-hz-mirrorcosu.acgvideo.com/upgcxcode/",
            "http://upos-hz-mirrorhw.acgvideo.com/upgcxcode/",
            "https://upos-hz-mirrorcosu.acgvideo.com/upgcxcode/",
            "https://upos-hz-mirrorks3u.acgvideo.com/upgcxcode/"
        ]
        try:
            if self.__html == "":
                raise Exception("getHTMLError")
            if self.__html.find(label[0]) == -1:
                for i in range(len(label)):
                    i = i + 1
                    if self.__html.find(label[i]) != -1:
                        loc = self.__html.find(label[i]) + len(label[i])
                        cid = self.__html[loc:loc + 25].split("/")[2]
                        break
                    elif i == len(label) - 1 and self.__html.find(
                            label[i] == -1):
                        raise Exception("findLabelError")
            else:
                loc = self.__html.find(label[0]) + len(label[0])
                cid = self.__html[loc:loc + 25].split("/")[2]
            if not cid.isnumeric():
                raise Exception("__getcidError")
            return cid
        except Exception as error:
            print("{}".format(error))
            return ""

    # 获取弹幕
    def getDanmaku(self):
        cid = self.__cid
        danmaku_url = r"https://api.bilibili.com/x/v1/dm/list.so?oid={}".format(
            cid)
        danmaku_html = VideoData.getHTMLText(danmaku_url)
        soup = bs.BeautifulSoup(danmaku_html, "html.parser")
        content = soup.findAll("d")
        danmaku = list()
        for each in content:
            danmaku.append(each.text)
        # 将弹幕保存到对应的视频文件夹
        if len(danmaku) is not 0:
            with open("{}/danmaku.txt".format(self.video_info["title"]),
                      "w",
                      encoding="utf-8") as file:
                for each in danmaku:
                    file.writelines(each + "\n")

    # 获取视频标签
    def getVideoTags(self):
        try:
            soup = bs.BeautifulSoup(self.__html, "html.parser")
            ul = soup.find("ul", {"class": "tag-area clearfix"})
            tags = list()
            for each in ul.children:
                if each.name == "li":
                    tag = each.find("a").string
                    tags.append(tag)
        except:
            tags = ""
        # 将标签保存到对应的视频文件夹
        if len(tags) is not 0:
            with open("{}/tags.txt".format(self.video_info["title"]),
                      "w",
                      encoding="utf-8") as file:
                for each in tags:
                    file.writelines(each + "\n")

    # 获取视频评论
    def getVideoComment(self):
        aid = self.__aid
        # 无aid号无法获取评论
        if aid is "":
            return ""

        # 获取热评，并写入对应视频文件夹的replies.txt
        def getHots():
            hots_file = open("{}/hots.txt".format(self.video_info["title"]),
                             "w",
                             encoding="utf-8")
            comment_url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid={}&sort=2".format(
                aid)
            print(comment_url)
            comment_html = requests.get(comment_url).text
            content = json.loads(comment_html)

            if content["data"]["hots"] is "null":
                hots_file.close()
                return
            try:
                hots_length = len(content["data"]["hots"])
                for i in range(hots_length):
                    hots_message = content["data"]["hots"][i]["content"][
                        "message"]
                    hots_file.write(hots_message + "\n")
                    if content["data"]["replies"][i]["replies"] is "null":
                        continue
                    length = len(content["data"]["hots"][i]["replies"])
                    for j in range(length):
                        hots_message_replies = content["data"]["hots"][i][
                            "replies"][j]["content"]["message"]
                        hots_file.write(hots_message_replies + "\n")
            except Exception as error:
                print(error)
                hots_file.close()
                return
            hots_file.close()

        def getReplies():
            pn = 2
            replies_file = open("{}/replies.txt".format(
                self.video_info["title"]),
                                "w",
                                encoding="utf-8")

            while True:
                comment_url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={}&type=1&oid={}&sort=2".format(
                    pn, aid)
                print(comment_url)
                comment_html = comment_html = requests.get(comment_url).text
                content = json.loads(comment_html)
                if (content["data"]["replies"] is "null"
                        or content["data"]["replies"] is None):
                    replies_file.close()
                    return
                try:
                    replies_length = len(content["data"]["replies"])
                    for i in range(replies_length):
                        comment_message = content["data"]["replies"][i][
                            "content"]["message"]
                        replies_file.write(comment_message + "\n")
                        if (content["data"]["replies"][i]["replies"] is "null"
                                or content["data"]["replies"][i]["replies"] is
                                None):
                            continue
                        length = len(content["data"]["replies"][i]["replies"])
                        for j in range(length):
                            comment_message_replies = content["data"][
                                "replies"][i]["replies"][j]["content"][
                                    "message"]
                            replies_file.write(comment_message_replies + "\n")
                except Exception as error:
                    print(error)
                    replies_file.close()
                    return
                pn += 1
            replies_file.close()

        getHots()
        getReplies()
        # t1 = threading.Thread(target=getHots, name="t1")
        # t2 = threading.Thread(target=getReplies, name="t2")
        # t1.start()
        # t2.start()

    # 获取视频弹幕，标签，评论
    def getVideoData(self):
        t1 = threading.Thread(target=self.getDanmaku, name="t1")
        t2 = threading.Thread(target=self.getVideoTags, name="t2")
        t3 = threading.Thread(target=self.getVideoComment, name="t3")
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()


if __name__ == "__main__":
    url = (
        "https://www.bilibili.com/video/av68733672?from=search&seid=17475276492885281451"
    )
    text = VideoData.getHTMLText(url)