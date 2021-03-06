#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : UiLIb.py
Author: Lewis Lau
Date  : 2017/11/16
Desc  :

    这里有个严重的设计问题，
    界面输出应该只到一个界面上，其他的界面仅仅是传递消息到界面的UI
    否者，在线程管理上非常麻烦
"""

# if __name__ == "__main__":
#    print ('Hello world"')


# coding=utf-8
fmt = '\033[0;3{}m{}\033[0m'.format

BLACK = 0  # 黑
RED = 1  # 红
GREEN = 2  # 绿
YELLOW = 3  # 棕
BLUE = 4  # 蓝
PURPLE = 5  # 紫
CYAN = 6  # 青
GRAY = 7  # 灰

'''
print fmt(color.BLACK, 'kzc')
print fmt(color.RED, 'kzc')
print fmt(color.GREEN, 'kzc')
print fmt(color.YELLOW, 'kzc')
print fmt(color.BLUE, 'kzc')
print fmt(color.PURPLE, 'kzc')
print fmt(color.CYAN, 'kzc')
print fmt(color.GRAY, 'kzc')
'''
class CPrint(object):
    @staticmethod
    def BLUE(*args):
        print fmt(BLUE , *args)

    @staticmethod
    def BLACK(*args):
        print fmt(BLACK , *args)

    @staticmethod
    def RED(*args):
        print fmt(RED, *args)

    @staticmethod
    def GREEN(*args):
        print fmt(GREEN, *args)

    @staticmethod
    def YELLOW(*args):
        print fmt(YELLOW, *args)

    @staticmethod
    def PURPLE(*args):
        print fmt(PURPLE, *args)

    @staticmethod
    def CYAN(*args):
        print fmt(CYAN, *args)

    @staticmethod
    def GRAY(*args):
        print fmt(GRAY, *args)