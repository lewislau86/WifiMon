#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : Utils.py.py
Author: Lewis Lau
Date  : 2017/11/16
Desc  :
"""

DESCRIPTION = "A command line tool for logging 802.11 probe request frames"
import sys
import logging
import argparse
import subprocess
import UiLIb

from InitEnv import singleton as Init
from Utils import singleton as Utils


#logging.basicConfig(level=logging.DEBUG)


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-i', '--interface', help="capture interface")
    parser.add_argument('-o', '--output', default='out.log', help="logging output location")
    return parser.parse_args()

#==========================================================

def parse_input(inputText):
    '''
    这里要解决：1，如果是数字则返回相关的网卡
        2，如果是网卡名字，则要检查是否正确（在我们的网卡列表中存在）
        返回值：网卡的准确设备名，失败返回None
    '''
    netCardName = None
    if inputText.isdigit():
        index = int(inputText)
        if index < len(Init.get_netcard_info()):
            netCardName = Init.get_netcard_info()[index][0]
    else:
        for i in range(len(Init.get_netcard_info())):
            if inputText.lower() == str(Init.get_netcard_info()[i][0]).lower():
                netCardName = str(Init.get_netcard_info()[i][0])
    return netCardName

def main():
    global  nicDev

    #if False == Init.get_check_result():
    #    sys.exit()

    args = parse_args()
    #logging.debug(args)
    # 这里应该避免输入错误 让用户直接选择网卡
    if not args.interface:
        infInput = raw_input(UiLIb.fmt(UiLIb.RED, "Enter the 'No' ro 'NIC' to sniffing it: "))
        nicDev = parse_input(infInput)
    else:
        nicDev = parse_input(args.interface)
    if None != nicDev:
        Utils.enableNICMonitorMode(nicDev)

if __name__ == "__main__":
    main()
