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
import logging
import UiLIb
import os
from Utils import singleton as Utils

#logging.basicConfig(level=logging.DEBUG)

cmd = [ ['scapy','-h'] ,
        ['airmon-ng','-h'] ]
#==========================================================

class checkEnv(object):
    __netcard_ip_info = []
    __netcard_mac_info = []
    __missing_info = []
    __err_permission = False
    __err_os = False
    __env_failed = False

    def __init__(self):
        self.__do_check()

    def __check_all(self):
        for i in range(len(cmd)):
            ret,_ = Utils.runCmd(cmd[i])
            if (0 != ret ):
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
        self.__netcard_ip_info , self.__netcard_mac_info = Utils.getNICInfo()
        return self.__netcard_ip_info , self.__netcard_mac_info



    def showInfo(self):
        if len(self.__missing_info)>0:
            UiLIb.CPrint.BLUE("===\tYou must install moudle as follow:")
            for i in range(len(self.__missing_info)):
                UiLIb.CPrint.GREEN(self.__missing_info[i])
            self.__env_failed = False
        else:
            UiLIb.CPrint.BLUE("===\tThe dependent module is installed.")

        if self.__err_permission:
            UiLIb.CPrint.BLUE("===\tCurrent user is not root.")
            self.__env_failed = False

        if self.__err_os:
            UiLIb.CPrint.BLUE("===\tMust run on GNU/Linux or Unix.")
            self.__env_failed = False

        UiLIb.CPrint.BLUE("===\tNetwork inforrmation:")
        UiLIb.CPrint.YELLOW("No\tNIC\t\t\t\tMac\t\t\t\tIpAddress\t\t")

        # 这里要修改下，因为有Mac地址不一定有IP
        for i in range(len(self.__netcard_mac_info)):
            ipStr = Utils.get_ip(self.__netcard_mac_info[i][0])
            UiLIb.CPrint.GREEN(str(i) + "\t" + self.__netcard_mac_info[i][0] + "\t\t\t" + self.__netcard_mac_info[i][1] + "\t\t" + ipStr )

        '''
        for i in range(len(self.__netcard_ip_info)):
            macstr = Utils.get_mac(self.__netcard_ip_info[i][0])
            if None != macstr:
                UiLIb.CPrint.GREEN(str(i) +"\t" + self.__netcard_ip_info[i][0] + "\t\t" + self.__netcard_ip_info[i][1] + "\t\t" + macstr)
        '''


    def __check_permission(self):
        return True if(os.getuid() != 0) else False

    def __check_os(self):
        return True if (os.uname()[0].startswith("Linux") and not "Darwin" not in os.uname()) else False



# ==========================================================
# 单例模式
singleton = checkEnv()