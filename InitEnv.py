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

#logging.basicConfig(level=logging.DEBUG)

cmd = [ ['scapy','-h'] ,
        ['airmon-ng','-h']]


class checkEnv(object):
    __netcard_info = []
    __missing_info = []
    __err_permission = False
    __err_os = False

    def __init__(self):
        pass

    def __check_cmd(self,cmd):
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ret = p.wait()
            return ret
        except OSError,e:
            return e.errno

    def __check_all(self):
        for i in range(len(cmd)):
            if (0 != self.__check_cmd(cmd[i])):
                logging.debug(cmd[i][0] + "\t Missing")
                self.__missing_info.append(cmd[i][0])
            else:
                logging.debug(cmd[i][0] + "\t  Installed")
        __err_permission = self.__check_permission()
        __err_os = self.__check_os()

    def do_check(self):
        self.__check_all()
        self.__get_netcard()
        self.showInfo()

    def __get_netcard(self):
        info = psutil.net_if_addrs()
        for k, v in info.items():
            for item in v:
                if item[0] == 2 and not item[1] == '127.0.0.1':
                    self.__netcard_info.append((k, item[1]))
        return self.__netcard_info

    def showInfo(self):
        if len(self.__missing_info)>0:
            print  UiLIb.fmt(UiLIb.BLUE, "===\tYou must install moudle as follow:\t===")
            for i in range(len(self.__missing_info)):
                print UiLIb.fmt(UiLIb.GREEN,self.__missing_info[i])
        else:
            print "===\tYThe dependent module is installed.\t==="

        print UiLIb.fmt(UiLIb.BLUE, "===\tNetwork inforrmation:\t===")
        print UiLIb.fmt(UiLIb.GREEN, self.__netcard_info)



    def __check_permission(self):
        return True if(os.getuid() != 0) else False

    def __check_os(self):
        return True if (os.uname()[0].startswith("Linux") and not "Darwin" not in os.uname()) else False

object = checkEnv()