#coding=utf-8
'''
    Initializing environment
    --------------------------------
    1. scapy
    2. airmon-ng
    3. Network interface

'''

import subprocess
import psutil

cmd = [ ['scapy','-h'] ,
        ['airmon-ng','-h']]


class checkEnv(object):
    @staticmethod
    def __check_cmd(cmd):
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ret = p.wait()
            return ret
        except OSError,e:
            return e.errno

    @staticmethod
    def __check_all():
        Missing = 0
        for i in range(len(cmd)):
            if (0 != checkEnv.__check_cmd(cmd[i])):
                print cmd[i][0] + "\t Missing"
                Missing = 1
            else:
                print cmd[i][0] + "\t  Installed"
        return Missing

    @staticmethod
    def do_check():
        if (0==checkEnv.__check_all()):
            print "ok"
        else:
            print "Missing install it"
        print  checkEnv.get_netcard()

    @staticmethod
    def get_netcard():
        netcard_info = []
        info = psutil.net_if_addrs()
        for k, v in info.items():
            for item in v:
                if item[0] == 2 and not item[1] == '127.0.0.1':
                    netcard_info.append((k, item[1]))
        return netcard_info