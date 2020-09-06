# -*- coding:utf-8 -*-
"""
使用正则表达式爬取微博热搜数据
"""
import os
import requests
import json
import time
from lxml import etree


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
    source = etree.HTML(text)
    trs = source.xpath('//tbody//tr[1]/following::tr')
    for tr in trs:
        number = tr.xpath('./td[1]/text()')
        href = tr.xpath('./td[2]/a/@href_to')
        if len(href) == 0:
            href = tr.xpath('./td[2]/a/@href')
        topic = tr.xpath("./td[2]/a/text()")
        popularity = tr.xpath("./td[2]/span/text()")

        yield {
            "number": number[0].strip(),
            "url": url_prefix.format(href[0].strip()),
            "topic": topic[0].strip(),
            "popularity": popularity[0].strip()
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
