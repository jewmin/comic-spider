# -*- coding: utf-8 -*-
import requests
import json
import time
from bs4 import BeautifulSoup
import download_pictures


def download_info():
    """ 下载列表页（包含所有对图片的描述信息），并存储到data/info.txt文件中 """
    chapter_list = []

    url = 'https://m.k886.net/comic/name/17種性幻想情侶遊戲/id/33109'
    rsp = requests.get(url)
    soup = BeautifulSoup(rsp.content, "html.parser")
    li_tag = soup.find("div", {"id": "chapterList"}).find_all("li")
    for li in li_tag:
        a = li.find("a")
        if a:
            chapter_list.append({"link": a["href"], "title": a["title"]})

    has_chapter_list = download_pictures.get_link_info()
    for chapter in chapter_list:
        if chapter["link"] in has_chapter_list:
            continue
        link = chapter["link"]
        chapter["list"] = []
        while link is not None:
            page_img, next_url = download_page(link)
            if page_img is None:
                time.sleep(5)
            else:
                chapter["list"].append(page_img)
                if next_url is not None:
                    link = next_url
                else:
                    break

        save_page(chapter)


def download_page(url):
    """ 下载某页面的信息 """
    page_img = None
    rsp = requests.get(url)
    if len(rsp.content) == 0:
        return None, None
    soup = BeautifulSoup(rsp.content, "html.parser")
    if len(soup.contents) == 0:
        return None, None

    img_tag = soup.find("div", {"id": "manga"}).find_all("img")
    for img in img_tag:
        if img.get("alt", None) is not None:
            page_img = img["src"]
            break

    next_url = None
    li_tag = soup.find("div", {"id": "action"}).find_all("li")
    for li in li_tag:
        a = li.find("a")
        if a and a.text == u"下一頁" and not a["href"].startswith("javascript"):
            next_url = a["href"]
            break

    return page_img, next_url


def save_page(chapter):
    """ 保存某页面的信息 """
    txt = json.dumps(chapter)
    with open('data/info.txt', 'a') as f:
        f.write(txt)
        f.write('\n')


if __name__ == "__main__":
    download_info()
