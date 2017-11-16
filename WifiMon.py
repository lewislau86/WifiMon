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
from Utils import singleton as Untils


#logging.basicConfig(level=logging.DEBUG)


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-i', '--interface', help="capture interface")
    parser.add_argument('-o', '--output', default='out.log', help="logging output location")
    return parser.parse_args()


def main():
    global  nicDev
    Init.do_check()
    #if False == Init.do_check():
    #    sys.exit()

    args = parse_args()
    #logging.debug(args)
    # 这里应该避免输入错误 让用户直接选择网卡
    if not args.interface:
        nicDev = raw_input(UiLIb.fmt(UiLIb.RED, "Enter the Name of the interface to sniff: "))
        print ("\n")
    else:
        nicDev = args.interface


if __name__ == "__main__":
    main()
