#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : PraseArg.py
Author: Lewis Lau
Date  : 2017/11/25
Desc  : 
"""

# if __name__ == "__main__":
#    print ('Hello world"')

import argparse
import UiLIb
from Utils import singleton as Utils

class parseArg(object):
    DESCRIPTION = "A command line tool for logging 802.11 probe request frames"
    __args = argparse.Namespace

    def parse_args(self):
        parser = argparse.ArgumentParser(description=parseArg.DESCRIPTION)
        parser.add_argument('-i', '--interface', help="capture interface")
        parser.add_argument('-o', '--output', default='out.log', help="logging output location")
        parser.add_argument('-a', '--access', default=False, help="Include AP's into the survey")
        return parser.parse_args()

    def parse_input(self, inputText):
        '''
        这里要解决：1，如果是数字则返回相关的网卡
            2，如果是网卡名字，则要检查是否正确（在我们的网卡列表中存在）
            返回值：网卡的准确设备名，失败返回None
        '''
        netCardName = None
        if inputText.isdigit():
            index = int(inputText)
            _, macList = Utils.getNICInfo()
            if index < len(macList):
                netCardName = str(macList[index][0])

        else:
            for i in range(len(Utils.getNICInfo())):
                if inputText.lower() == str(Utils.getNICInfo()[i][0]).lower():
                    netCardName, _ = str(Utils.getNICInfo()[i][0])
        return netCardName

    def do_parse(self):
        self.__args = self.parse_args()
        if not self.__args.interface:
            try:
                # do while
                while True:
                    infInput = raw_input(UiLIb.fmt(UiLIb.PURPLE, "Enter the 'No' ro 'NIC' to sniffing it: "))
                    dev = self.parse_input(infInput)
                    if dev != None:
                        break
                    else:
                        UiLIb.CPrint.RED("Error input, try again")
            except KeyboardInterrupt:
                UiLIb.CPrint.GREEN("\n\n\t****** Good Bye ******\n\n")
                sys.exit(0)
        else:
            dev = self.parse_input(args.interface)
        return dev

    def get_parse(self):
        return self.__args

# ==========================================================
# 单例模式
singleton = parseArg()