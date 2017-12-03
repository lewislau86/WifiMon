#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : Command.py
Author: Lewis Lau
Date  : 2017/12/3
Desc  : 
"""

from Common import singleton as Status
import UiLIb

class Command(object):
    def entry(self):
        Status.setMode(Status.cmdMode)
        self.get_cmd()
        pass

    def leave(self):
        Status.setMode(Status.verboseMode)
        pass

    def prompt(self):
        pass

    def get_cmd(self):
        cmd = raw_input(UiLIb.fmt(UiLIb.PURPLE, "[cmd] >>>: "))
        return cmd

    def get_status(self):
        pass





# ==========================================================
# 单例模式
singleton = Command()