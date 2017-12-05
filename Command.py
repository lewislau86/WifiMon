#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : Command.py
Author: Lewis Lau
Date  : 2017/12/3
Desc  : 
"""
import Common
from Verbose import singleton as Verbase
import UiLIb
import sys

class Status(object):
    verboseMode = 1
    cmdMode = 2
    __currentMode = 0

    def getCurrentMode(self):
        return self.__currentMode

    def setMode(self , mode):
        if mode==1 or mode==2:
            self.__currentMode = mode


class Command(object):
    __status = Status()
    def __init__(self):
        self.__status.setMode(self.__status.verboseMode)

    def entry(self):
        if self.__status.verboseMode == self.__status.getCurrentMode():
            self.__status.setMode(self.__status.cmdMode)
            Verbase.setSilent(True)
        elif Status.cmdMode == Status.getCurrentMode():
            # 如果已经在命令模式，仍然Ctrl+, 则退出
            sys.exit(0)
        else:
            UiLIb.CPrint.YELLOW("Uninitialized!\r\n")

        self.cmd_loop()

    def leave(self):
        self.__status.setMode(self.__status.verboseMode)
        Verbase.setSilent(False)

    def prompt(self):
        UiLIb.CPrint.BLUE(Common.CmdInfo)

    def cmd_loop(self):
        while True:
            if self.__status.getCurrentMode() == self.__status.verboseMode:
                break
            cmd = self.get_cmd()
            if cmd in ["save","attack","exit","verbose","export"]:
                self.cmd_handle(cmd)
            else:
                UiLIb.CPrint.RED("invalid command")

    def cmd_handle(self,cmd):
        if "save" == cmd:
            self.cmd_handle_save()
        elif "attack" == cmd:
            self.cmd_handle_attack()
        elif "exit" == cmd:
            self.cmd_handle_exit()
        elif "verbose" == cmd:
            self.leave()
        elif "export" == cmd:
            self.cmd_handle_export()
        elif "help" == cmd:
            self.prompt()
        else:
            UiLIb.CPrint.PURPLE("\n\t\tError command\r\n")

    def cmd_handle_exit(self):
        sys.exit(0)

    def cmd_handle_save(self):
        UiLIb.CPrint.PURPLE("\n\t\tSave\r\n")

    def cmd_handle_attack(self):
        pass

    def cmd_handle_export(self):
        pass

    def get_cmd(self):
        self.prompt()
        cmd = raw_input(UiLIb.fmt(UiLIb.PURPLE, ">>>: "))
        return cmd

    def get_status(self):
        pass





# ==========================================================
# 单例模式
singleton = Command()