#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# undone

from urllib import parse
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from spider.constant import *


def get_filename(keyword):
    pos = '../data/question_list/'
    form = '.csv'
    return pos + keyword + form


def get_url(keyword):
    # 基于关键词检索, 返回展开后的url链接
    print("(一) 编码关键词 <" + keyword + "> 中...")
    base_url = "https://www.youtube.com/results?search_query="
    url = base_url + parse.quote(keyword, safe='/', encoding='utf-8')
    print("编码成功, url链接: " + url)
    return url


def page_shake(driver):
    # 为防止页面本身出bug, 置底后向上滑动一次, 再置底, 保证页面的动态加载过程
    driver.execute_script(to_bottom)  # 将滚动条移动到页面的底部
    time.sleep(sleep_time)
    driver.execute_script(to_top)
    ###


def get_html(url):
    # 基于web driver来应对知乎的动态加载措施
    print("(二) 访问页面中...")
    driver = webdriver.Firefox()    # 打开浏览器
    driver.get(url)     # 打开网页 - 知乎关键词检索后的网页
    page_shake(driver)
    for i in range(max_num):
        time.sleep(sleep_time)
        driver.execute_script(to_bottom)  # 将滚动条移动到页面的底部
        print("正在进行第" + str(i+1) + "次置底操作...")
        i += 1

    html = driver.page_source  # get html
    driver.close()
    print("成功访问, 已获取html源码")
    return html


def get_comments_list(url):
    # 由url链接获取所有相关提问的列表
    html = get_html(url)
    soup = BeautifulSoup(html, features='lxml')

    print("(三) 数据处理中...")
    comments = soup.find_all('ytd-comment-thread-renderer', {'class': 'style-scope ytd-item-section-renderer'})

    comments_list = []
    for comment in comments:
        comment_author = comment.find('a', {'id': 'author-text'}).get_text().strip()
        comment_content = comment.find('div', {'id': 'content'}).get_text()
        comments_list.append({'author': comment_author, 'content': comment_content})

    print("已成功解析出所有相关问题列表")
    return comments_list


def save2csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, sep=',', header=True, index=True, encoding='utf-8')
    print("(四) 数据已保存在 <" + filename + "> ...")


def spider(keyword):
    print("开始检索关键字 <" + keyword + ">...")
    filename = get_filename(keyword)
    url = get_url(keyword)
    question_list = get_question_list(url)
    save2csv(question_list, filename)
    print("完成检索")


def main():
    spider("这就是街舞")


if __name__ == 'main':
    main()



