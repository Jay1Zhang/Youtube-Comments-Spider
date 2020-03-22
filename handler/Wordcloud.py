#!/usr/bin/env python
# -*- coding:utf-8 -*-


import re               # 正则表达式库
import collections      # 词频统计库
import numpy as np      # numpy数据处理库
import jieba            # 结巴分词
import wordcloud        # 词云展示库
from PIL import Image   # 图像处理库
import matplotlib.pyplot as plt # 图像展示库


# 1. 读取文本文件, 并进行一定的文本预处理
def get_clear_text(filename):
    # 读取文件
    with open(filename, encoding='utf-8') as f:    # 此处如果用 utf-8 打开会有问题
        text = f.read()
    # 利用正则进行数据清洗
    pattern = re.compile(u'[\t\n\r\.\-\+:;\(\)\?\"\'\^] |'      # 英文字符
                         u'[，。？（）【】—：；…“”]')         # 中文字符
    text = re.sub(pattern, '', text)                              # 清除
    return text


# 2. 文本分词
def seg_word(text):
    seg_list = jieba.cut(text, cut_all = False, HMM=True) # 精确模式 + HMM模式分词
    # 自定义去除词库
    remove_words = [u'的', u'和', u'了', u'呢', u'是', u'等',u'能',u'都', u'中', u'在',
                    u'我', u'你', u'他', u'她', u'它', u'这', u'那',
                    u'，', u'“', u'”', u'"', u'。', u'\n', u'不', u' ', u',', u'、',
                    u'！', u'有', u'就', u'要', u'说', u'也', u'就是', u'吗', u'吧', u'对',
                    u'去',  u'不是', u'好', u'被', u'没有', u'什么', u'很', u'还', u'啊', u'可以',
                    u'知道',  u'-', u'一个', u'给', u'看', u'但是', u'想', u'会', u'到', u'做',
                    u'觉得', u'那些', u'这', u'不要', u'这么', u'跟', u'把', u'年', u'让', u'真的',
                    u'多', u'着', u'而', u'怎么', u'没', u'这个', u'来', u'这些', u'但', u'如果',
                    u'!', u'地', u'上', u'只是', u'又', u'过', u'才', u'搞', u'用', u'得', u'这样',
                    u'看到', u'很多', u'事情', u'.', u'?', u'时候', u'事', u'~', u'唔',
                    u'人', u'你们', u'我们', u'他们',
                    ]

    word_list = []
    for word in seg_list:
        if word not in remove_words:    # 如果不在去除词库中
            word_list.append(word)      # 分词追加到列表

    return word_list


# 3. 词频统计
def word_freq_count(word_list):
    word_count = collections.Counter(word_list)     # 对分词做词频统计
    word_count_top10 = word_count.most_common(10)   # 获取前10最高频的词
    # print(word_counts)
    print(word_count_top10)    # 输出检查
    return word_count


# 4. 生成词云
def generate_wordcloud(word_count, output_path):
    mask = np.array(Image.open('timg.jfif'))  # 定义词频背景
    image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案

    wc = wordcloud.WordCloud(
        font_path='simhei.ttf',     # 设置字体格式
        mask=mask,                  # 设置背景图
        max_words=200,              # 最多显示词数
        max_font_size=100,          # 字体最大值
        background_color="white"
    )
    wc.generate_from_frequencies(word_count)            # 从字典生成词云
    # wc.recolor(color_func=image_colors)                 # 将词云颜色设置为背景图方案

    plt.imshow(wc)      # 显示词云
    plt.axis('off')     # 关闭坐标轴
    plt.savefig(output_path)
    plt.show()          # 显示图像


def generate_wordcloud_from_file(filename, output_path):
    text = get_clear_text(filename)
    word_list = seg_word(text)
    word_count = word_freq_count(word_list)
    generate_wordcloud(word_count, output_path)


def main():
    generate_wordcloud_from_file("../data/comments_list/HongKong.csv", "../data/wordcloud/WordCloud.jpg")


if __name__ == 'main':
    main()


main()
