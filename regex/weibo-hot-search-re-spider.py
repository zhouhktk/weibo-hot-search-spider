# -*- coding:utf-8 -*-
"""
使用正则表达式爬取微博热搜数据
"""
import os
import re
import requests
import json
import time


def weibo_top_page(url):
    """
    获取热搜榜页面
    :param url: 热搜榜链接
    :return: 热搜榜网页
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    try:
        res = requests.get(url=url, headers=headers)
    except requests.exceptions.RequestException:
        print("Error")
        return None
    else:
        res.encoding = res.apparent_encoding
        return res.text


def weibo_top_parse(text):
    """
    解析网页，得到话题字典
    :param text: 网页
    :return: 话题字典
    """
    url_prefix = "https://s.weibo.com{}"
    tops_pattern = re.compile('<tbody>(.*?)</tbody>', re.S)
    tops_text = re.findall(tops_pattern, text)[0]
    topics_pattern = re.compile('<tr class="".*?>(.*?)</tr>', re.S)
    topics = re.findall(topics_pattern, tops_text)
    for topic in topics:
        topic = re.findall('<td class="td-01 ranktop">(.*?)</td>.*?'
                           '<a href.*?="(.*?)".*?>(.*?)</a>.*?<span>(.*?)</span>', topic, re.S)
        if len(topic) > 0:
            yield {
                "number": topic[0][0].strip(),
                "url": url_prefix.format(topic[0][1].strip()),
                "topic": topic[0][2].strip(),
                "popularity": topic[0][3].strip()
            }


def write_to_json(content):
    """
    将数据写入json文件
    :param content:
    :return:
    """
    dir_prefix = r"E:/PyCharm/weibo-hot-search-data"

    file_path = time.strftime('%Y{}/%m{}/%d{}', time.localtime()).format("年", "月", "日")
    file_path = os.path.join(dir_prefix, file_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    name = time.strftime('%H{}.json', time.localtime()).format("时")
    file_name = os.path.join(file_path, name)
    with open(file_name, 'w', encoding='utf-8') as f:
        # json.dumps()将字典序列化
        # ensure_ascii = False保证输出的结果是中文而不是Unicode码
        f.write(json.dumps(content, ensure_ascii=False, indent=2))


def main():
    url = "https://s.weibo.com/top/summary"
    page = weibo_top_page(url)
    results = weibo_top_parse(page)
    data = []
    for res in results:
        data.append(res)
    write_to_json(data)


if __name__ == '__main__':
    main()
