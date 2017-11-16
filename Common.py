#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : Common.py
Author: Lewis Lau
Date  : 2017/11/16
Desc  : 
"""
import subprocess

# if __name__ == "__main__":
#    print ('Hello world"')


def runCmd(cmd):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ret = p.wait()
        return ret
    except OSError, e:
        return e.errno