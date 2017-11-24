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

DESCRIPTION = "A command line tool for logging 802.11 probe request frames"
import sys
import logging
import argparse
import subprocess
import UiLIb
from Utils import  singleton as Utils
from InitEnv import singleton as Init
from PacketParse import  singleton as Packet


#logging.basicConfig(level=logging.DEBUG)


#==========================================================
# Function
def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-i', '--interface', help="capture interface")
    parser.add_argument('-o', '--output', default='out.log', help="logging output location")
    return parser.parse_args()

def parse_input(inputText):
    '''
    这里要解决：1，如果是数字则返回相关的网卡
        2，如果是网卡名字，则要检查是否正确（在我们的网卡列表中存在）
        返回值：网卡的准确设备名，失败返回None
    '''
    netCardName = None
    if inputText.isdigit():
        index = int(inputText)
        if index < len(Utils.getNICInfo()):
            _,macList = Utils.getNICInfo()
            netCardName = str(macList[index][0])

    else:
        for i in range(len(Utils.getNICInfo())):
            if inputText.lower() == str(Utils.getNICInfo()[i][0]).lower():
                netCardName,_ = str(Utils.getNICInfo()[i][0])
    return netCardName

def main():
    global  nicDev

    #if False == Init.get_check_result():
    #    sys.exit()

    args = parse_args()
    #logging.debug(args)
    # 这里应该避免输入错误 让用户直接选择网卡
    if not args.interface:
        try:
            # do while
            while True:
                infInput = raw_input(UiLIb.fmt(UiLIb.PURPLE, "Enter the 'No' ro 'NIC' to sniffing it: "))
                nicDev = parse_input(infInput)
                if nicDev != None:
                    break
                else:
                    UiLIb.CPrint.RED("Error input, try again")
        except KeyboardInterrupt:
            UiLIb.CPrint.GREEN("\n\n\t****** Good Bye ******\n\n")
            sys.exit(0)
    else:
        nicDev = parse_input(args.interface)

    if None != nicDev:
        UiLIb.CPrint.GREEN("Monitor mode status :" + str(Utils.enableNICMonitorMode(nicDev)))

    if True ==  Utils.getNICMonitorMode(nicDev):
        print "start sniff"
        Packet.do_sniff()




#==========================================================
# Global
if __name__ == "__main__":
    main()
