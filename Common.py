#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : Common.py
Author: Lewis Lau
Date  : 2017/11/16
Desc  :
    这里主要保存程序版本号
    帮助信息

"""
# if __name__ == "__main__":
#    print ('Hello world"')
Version = "0.10"

HelpInfo = "Help"

CmdInfo = "Command\r\n" \
          "-h,--help\t\t\t Show help information"


class Status(object):
    verboseMode = 1
    cmdMode = 2
    __currentMode = 0

    def getCurrentMode(self):
        return self.__currentMode

    def setMode(self , mode):
        if mode==1 or mode==2:
            self.__currentMode = mode


# ==========================================================
# 单例模式
singleton = Status()
#==========================================================


