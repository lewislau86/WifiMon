#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : Verbose.py
Author: Lewis Lau
Date  : 2017/12/3
Desc  :
        缓存输出信息
        控制输出频率
        控制输出类型
        日志持久化 CSV格式

        vPrint 屏幕输出，不保存日志
        vLog   屏幕输出，保存日志（类型，内容）
"""

import csv
import time
import thread
import os
from PraseArg import singleton as PraseArg

class Verbose(object):
    __silent = False        # silent mode cache output
    __ApInfo = []
    __Client = []
    __silent_ApInfo = [] # manufacture, mac, crypto, ssid
    __silent_Client = [] # manufacture, mac, ssid
    __csvClientName = ""
    __csvAPName = ""
    __args = PraseArg.get_parse()

    fmt = '\033[0;3{}m{}\033[0m'.format

    cBLACK = 0  # 黑
    cRED = 1  # 红
    cGREEN = 2  # 绿
    cYELLOW = 3  # 棕
    cBLUE = 4  # 蓝
    cPURPLE = 5  # 紫
    cCYAN = 6  # 青
    cGRAY = 7  # 灰

    def __init__(self):
        currrntTime = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
        if False==os.path.exists("./output/"):
            os.makedirs("./output/")
        self.__csvClientName = "./output/Client-"+currrntTime+".csv"
        self.__csvAPName = "./output/AP-"+currrntTime+".csv"


    def silentModeThread(self ,id):
        # 静默模式只缓存输出到屏幕的信息
        while True:
            time.sleep(1)
            if False == self.__silent:
                thread.exit_thread()

    def setSilent(self , flag):
        if True == flag:
            self.entrySilent()
        else:
            self.leaveSilent()
        self.__silent = flag

    def entrySilent(self):
        thread.start_new_thread(self.silentModeThread , (1,))
        pass

    # 离开静默模式，要快速显示缓存的数据
    def leaveSilent(self):
        pass

    #UiLIb.CPrint.YELLOW('[Client:' + manufacture + '/' + mac + '] [SSID:' + ssid_probe.decode("utf-8") + ']')
    #UiLIb.CPrint.BLUE('[AP:' + manufacture + '/' + mac + '] ['+crypto+'] ['+'SSID:'+ ssid_probe.decode("utf-8") + ']')

    def vLogAP(self, manufacture, mac, crypto,ssid):
        # 写日志不受屏幕输出的影响
        output = '[AP:' + manufacture + '/' + mac + '] ['+crypto+'] ['+'SSID:'+ ssid + ']'
        self.vLogAPWrite(manufacture,mac,crypto,ssid)
        tmpAP = dict()
        tmpAP['mac'] = mac
        tmpAP['crypto'] = crypto
        tmpAP['ssid'] = ssid

        self.__ApInfo.append(tmpAP)

        if self.__silent == False:
            # normal
            self.vPrint(self.cBLUE , output)
        self.vLogAPWrite(manufacture,mac,crypto,ssid)

    def vLogHiddenAP(self,manufacture, mac, crypto,ssid):
        pass

    def vLogClient(self, manufacture, mac, ssid):
        if self.__args.fake == False:
            output = '[Client:' + manufacture + '/' + mac + '] [SSID:' + ssid + ']'
            self.vLogClientWrite(manufacture,mac,ssid)

            if self.__silent == False:
                # normal
                self.vPrint(self.cYELLOW, output)
            self.vLogClientWrite(manufacture,mac,ssid)


    def vLogAPWrite(self, manufacture,mac,crypto,ssid):
        fpcsv = open(self.__csvAPName, 'a')  # 设置newline，否则两行之间会空一行
        writer = csv.writer(fpcsv)
        writer.writerow([manufacture,mac,crypto,ssid])
        fpcsv.close()

    def vLogClientWrite(self, manufacture,mac,ssid):
        fpcsv = open(self.__csvClientName, 'a')  # 设置newline，否则两行之间会空一行
        writer = csv.writer(fpcsv)
        writer.writerow([manufacture,mac,ssid])
        fpcsv.close()


    def vPrint(self, color , *args):
        if 0<=color and color<=7:
            print self.fmt(color, *args)
    # 程序退出时，快速写日志
    def flush(self):
        pass

    def get_apInfo(self):
        return self.__ApInfo


# ==========================================================
# 单例模式
singleton = Verbose()