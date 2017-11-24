#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : Utils.py.py
Author: Lewis Lau
Date  : 2017/11/16
Desc  : 
"""
#==========================================================
# Define
import subprocess
import psutil
#==========================================================

class Utils(object):
    __ip_info = []
    __mac_info = []
    def __init__(self):
        self.__getNICInfo()

    def enableNICMonitorMode(self , nicDev):
        if False == self.getNICMonitorMode(nicDev):
            print " Setting Wireless card into Monitor Mode"
            if 'mon' not in nicDev:
                cmd = ['airmon-ng', 'start',nicDev]
                print cmd
                ret, _ = self.runCmd(cmd)
                if 0 == ret:
                    return True
        else:
            return False

    def getNICMonitorMode(self,nicDev):
        if "mon" in  nicDev:
            return True
        else:
            monDev = str(nicDev)+"mon"
            del self.__ip_info[:]
            del self.__mac_info[:]
            self.__getNICInfo()
            for i in range(len(self.__mac_info)):
                if monDev==self.__mac_info[1][0]:
                    return  True
            return False


    def __getNICInfo(self):
        info = psutil.net_if_addrs()
        for k, v in info.items():
            for item in v:
                '''
                    这里有点问题，关于MAC地址类型，在MAC下是18，在Kali下是17
                '''
                if item[0] == 18 or item[0] == 17:
                    self.__mac_info.append((k, item[1]))
                if item[0] == 2:
                    self.__ip_info.append((k, item[1]))

    def getNICInfo(self):
        return self.__ip_info , self.__mac_info

    def get_mac(self,intf):
        for i in range(len(self.__mac_info)):
            if (intf == self.__mac_info[i][0]):
                return self.__mac_info[i][1]
        return ""

    def get_ip(self,intf):
        for i in range(len(self.__ip_info)):
            if (intf == self.__ip_info[i][0]):
                return self.__ip_info[i][1]
        return ""

    def runCmd(self , cmd):
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ret = p.wait()
            if p.returncode == 0:
                return ret, p.stdout.read()
            else:
                return ret, None
        except OSError, e:
            return e.errno, None

# ==========================================================
# 单例模式
singleton = Utils()

#==========================================================
# if __name__ == "__main__":
#    print ('Hello world"')
