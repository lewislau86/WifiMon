#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : Utils.py.py
Author: Lewis Lau
Date  : 2017/11/16
Desc  : 
"""

# if __name__ == "__main__":
#    print ('Hello world"')

class Utils(object):
    def enableNICMonitorMode(self,nicDev):
        if "mon" not in nicDev:  # yes i know this doesnt work with ubuntu/mint at the mo...
            print " Setting Wireless card into Monitor Mode"
            '''
            if 'mon' not in getWirelessInterfacesList():
            cmd = ['airmon-ng', 'start' ,intf]
          
            intf = intf + 'mon'

            '''

singleton = Utils()
