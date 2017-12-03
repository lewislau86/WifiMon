#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : Command.py
Author: Lewis Lau
Date  : 2017/12/3
Desc  : 
"""
import Common
from Common import singleton as Status
import UiLIb
import sys

class Command(object):
    def entry(self):
        if Status.verboseMode == Status.getCurrentMode():
            Status.setMode(Status.cmdMode)
        elif Status.cmdMode == Status.getCurrentMode():
            # 如果已经在命令模式，仍然Ctrl+, 则退出
            sys.exit(0)
        else:
            UiLIb.CPrint.YELLOW("Uninitialized!\r\n")

        self.cmd_loop()
        pass

    def leave(self):
        Status.setMode(Status.verboseMode)
        pass

    def prompt(self):
        UiLIb.CPrint.BLUE(Common.CmdInfo)
        pass

    def cmd_loop(self):
        while True:
            cmd = self.get_cmd()
            if cmd in ["aa","ss"]:
                print cmd
            else:
                print "cmd error"


    def get_cmd(self):
        self.prompt()
        cmd = raw_input(UiLIb.fmt(UiLIb.PURPLE, "[cmd] >>>: "))
        return cmd

    def get_status(self):
        pass





# ==========================================================
# 单例模式
singleton = Command()