# -*- coding: utf-8 -*-
import os
from download_pictures import get_info, get_info_imgs, download
import config

def generate_html(imgs):
    """ 生成html """
    content = {}
    for img in imgs:
        _, _, filepath, title = img
        if title in content:
            content[title] += u'<img src="' + filepath[5:] + u'" /><br />'
        else:
            content[title] = u'<img src="' + filepath[5:] + u'" /><br />'

    items = content.items()
    items.sort()
    prev_chapter = "javascript:;"
    for title, chapter in items:
        content[title] = u'<html><head><title>' + title + u'</title></head><body>' + chapter + u'<a style="font-size:18px;" href="' + prev_chapter + u'">上一页</a>'
        prev_chapter = title + '.html'
    items = content.items()
    items.sort(reverse=True)
    next_chapter = "javascript:;"
    for title, chapter in items:
        content[title] = chapter + u'<a style="font-size:18px;" href="' + next_chapter + u'">下一页</a></body></html>'
        next_chapter = title + '.html'
    for title, chapter in content.iteritems():
        html = os.path.join("data", config.config["dir"], title + '.html')
        with open(html, 'wb') as f:
            f.write(chapter.encode("gbk"))
            print('end generate', title)

if __name__ == '__main__':
    info = get_info()
    imgs = get_info_imgs(info)
    generate_html(imgs)
