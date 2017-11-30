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

import sys
import logging
import time
import subprocess
import UiLIb
from Utils import  singleton as Utils
from InitEnv import singleton as Init
from PraseArg import singleton as PraseArg
from PacketParse import  singleton as Packet


#logging.basicConfig(level=logging.DEBUG)

#==========================================================
# Function



def main():

    #if False == Init.get_check_result():
    #    sys.exit()

    nicDev = PraseArg.do_parse()
    if None != nicDev and False == Utils.getNICMonitorMode(nicDev):
        UiLIb.CPrint.GREEN("Monitor mode status :" + str(Utils.enableNICMonitorMode(nicDev)))
    time.sleep(0.5)
    if True ==  Utils.getNICMonitorMode(nicDev):
        Packet.do_sniff(nicDev)
    else
        print("Monitor Mode False")



#==========================================================
# Global
if __name__ == "__main__":
    main()
