import bs4 as bs
import requests
import pandas as pd
from videodata import VideoData
import os


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


def getRank(url=None, rank_type="all"):
    rank_types = {
        "all": "https://www.bilibili.com/ranking/all/0/0/3",
        "origin": "https://www.bilibili.com/ranking/origin/0/0/3",
        "bangumi": "https://www.bilibili.com/ranking/bangumi/13/0/3",
        "cinema": "https://www.bilibili.com/ranking/cinema/177/0/3",
        "rookie": "https://www.bilibili.com/ranking/rookie/0/0/3",
    }

    num_list = list()
    url_list = list()
    title_list = list()
    play_list = list()
    view_list = list()
    author_list = list()
    pts_list = list()
    rank = dict()

    if url == None:
        url = rank_types.get(rank_type)

    print(url)
    html = getHTMLText(url)
    soup = bs.BeautifulSoup(html, "html.parser")
    rank_list = soup.find("ul", {"class": "rank-list"}).children

    # 从html获取排行榜信息
    for li in rank_list:
        num_list.append(li.find("div", {"class": "num"}).text)
        url_list.append(li.find("a").get("href"))
        title_list.append(li.find("div", {"class": "info"}).a.text)
        play_list.append(li.findAll("span", {"class": "data-box"})[0].text)
        view_list.append(li.findAll("span", {"class": "data-box"})[1].text)
        author_list.append(li.findAll("span", {"class": "data-box"})[2].text)
        pts_list.append(li.find("div", {"class": "pts"}).find("div").text)

    rank["num"] = num_list
    rank["url"] = url_list
    rank["title"] = title_list
    rank["play"] = play_list
    rank["view"] = view_list
    rank["author"] = author_list
    rank["pts"] = pts_list

    day_rank_df = pd.DataFrame(rank)
    day_rank_df.to_csv("{}.csv".format(rank_type),
                       index=rank["num"],
                       encoding="utf-8")


if __name__ == "__main__":
    os.chdir(r"bilibili_data")
    getRank(rank_type="bangumi")
