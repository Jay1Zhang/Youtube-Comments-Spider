#!/usr/bin/env python 
# -*- coding:utf-8 -*-


import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from spider.constant import *


def get_filename(title):
    pos = '../data/comments_list/'
    title = title.replace('?', '')  # 文件名中不能有英文问号
    form = '.csv'
    return pos + title + form


def page_shake(driver):
    # 为防止页面本身出bug, 置底后向上滑动一次, 再置底, 保证页面的动态加载过程
    driver.execute_script(to_bottom)  # 将滚动条移动到页面的底部
    time.sleep(sleep_time)
    driver.execute_script(to_top)
    ###


def get_html(url):
    # 基于web driver来应对知乎的动态加载措施
    print("(一) 访问页面中...")
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
    # 由url链接获取该问题下所有回答的列表
    html = get_html(url)
    soup = BeautifulSoup(html, features='lxml')

    print("(二) 数据处理中...")
    comments = soup.find_all('ytd-comment-thread-renderer', {'class': 'style-scope ytd-item-section-renderer'})

    comments_list = []
    for comment in comments:
        comment_author = comment.find('a', {'id': 'author-text'}).get_text().strip()
        comment_content = comment.find('div', {'id': 'content'}).get_text()
        comments_list.append({'author': comment_author, 'content': comment_content})

    print("已成功解析出该问题下所有的回答列表")
    return comments_list


def save2csv(data, filename):
    df = pd.DataFrame(data, columns=['author', 'content'])
    df.to_csv(filename, sep=',', header=True, index=True, encoding='utf-8')
    print("(三) 数据已保存在 <" + filename + "> ...")


def spider(title, url):
    print("开始收集视频 <" + title + "> 下所有评论...")
    filename = get_filename(title)
    comments_list = get_comments_list(url)
    save2csv(comments_list, filename)
    print("完成收集, 结束进程")


def main():
    spider("香港尖沙咀遊行抗議", "https://www.youtube.com/watch?v=SoNXieilVlo")


main()

