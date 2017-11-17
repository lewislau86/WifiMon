#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : Utils.py.py
Author: Lewis Lau
Date  : 2017/11/16
Desc  :
    Initializing environment
    --------------------------------
    1. scapy
    2. airmon-ng
    3. Network interface
"""

import subprocess
import psutil
import logging
import UiLIb
import os
import Common

#logging.basicConfig(level=logging.DEBUG)

cmd = [ ['scapy','-h'] ,
        ['airmon-ng','-h'] ]


class checkEnv(object):
    __netcard_info = []
    __missing_info = []
    __err_permission = False
    __err_os = False
    __env_failed = False

    def __init__(self):
        self.__do_check()

    def __check_all(self):
        for i in range(len(cmd)):
            if (0 != Common.runCmd(cmd[i])):
                logging.debug(cmd[i][0] + "\t Missing")
                self.__missing_info.append(cmd[i][0])
            else:
                logging.debug(cmd[i][0] + "\t  Installed")
        self.__err_permission = self.__check_permission()
        self.__err_os = self.__check_os()

    def __do_check(self):
        self.__check_all()
        self.__get_netcard()
        self.showInfo()

    def get_check_result(self):
        return self.__env_failed

    def get_netcard_info(self):
        return self.__netcard_info
    '''
    # 这种方法不一定准确
    def getWirelessInterfacesList():
        networkInterfaces=[]        
        command = ["iwconfig"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        (stdoutdata, stderrdata) = process.communicate();
        output = stdoutdata
        lines = output.splitlines()
        for line in lines:
                if(line.find("IEEE 802.11")!=-1):
                        networkInterfaces.append(line.split()[0])
        return networkInterfaces
    '''
    def __get_netcard(self):
        info = psutil.net_if_addrs()
        for k, v in info.items():
            for item in v:
                if item[0] == 2:
                    self.__netcard_info.append((k, item[1]))
        return self.__netcard_info


    def showInfo(self):
        if len(self.__missing_info)>0:
            print  UiLIb.fmt(UiLIb.BLUE, "===\tYou must install moudle as follow:")
            for i in range(len(self.__missing_info)):
                print UiLIb.fmt(UiLIb.GREEN,self.__missing_info[i])
            self.__env_failed = False
        else:
            print UiLIb.fmt(UiLIb.BLUE, "===\tThe dependent module is installed.")

        if self.__err_permission:
            print UiLIb.fmt(UiLIb.BLUE, "===\tCurrent user is not root.")
            self.__env_failed = False

        if self.__err_os:
            print UiLIb.fmt(UiLIb.BLUE, "===\tMust run on GNU/Linux or Unix.")
            self.__env_failed = False

        print UiLIb.fmt(UiLIb.BLUE, "===\tNetwork inforrmation:")
        print UiLIb.fmt(UiLIb.YELLOW, "No\tNIC\t\tIPAddr\t\t")
        for i in range(len(self.__netcard_info)):
            print UiLIb.fmt(UiLIb.GREEN,str(i)+"\t"+self.__netcard_info[i][0]+"\t\t"+self.__netcard_info[i][1]+"\t\t")

    def __check_permission(self):
        return True if(os.getuid() != 0) else False

    def __check_os(self):
        return True if (os.uname()[0].startswith("Linux") and not "Darwin" not in os.uname()) else False

# 单例模式
singleton = checkEnv()