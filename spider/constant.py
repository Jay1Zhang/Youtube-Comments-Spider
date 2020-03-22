#!/usr/bin/env python 
# -*- coding:utf-8 -*-

to_bottom = "var q=document.documentElement.scrollTop=100000"  # 置底操作
to_top = "var q=document.documentElement.scrollTop=0"    # 置顶操作
max_num = 100       # 置底操作次数
sleep_time = 5      # 每隔一定时间进行一次置底操作, 以预留出网页加载时间，由于是外网，所以增加了时长
