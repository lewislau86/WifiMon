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
import threading
import time
import signal
import os
class Status(object):
    verboseMode = 1
    cmdMode = 2
    __currentMode = 0

    def getCurrentMode(self):
        return self.__currentMode

    def setMode(self , mode):
        if mode==1 or mode==2:
            self.__currentMode = mode


class Command(threading.Thread):
    __status = Status()

    def __init__(self,*args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True
        self.__status.setMode(self.__status.verboseMode)

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            self.entry()
            time.sleep(1)

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.leave()
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False


    def entry(self):
        if self.__status.verboseMode == self.__status.getCurrentMode():
            self.__status.setMode(self.__status.cmdMode)
            Verbase.setSilent(True)
        elif Status.cmdMode == Status.getCurrentMode():
            #sys.exit(0)
            pass
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
        self.stop()
        time.sleep(3)
        os._exit(0)

    def cmd_handle_save(self):
        UiLIb.CPrint.PURPLE("\n\t\tSave\r\n")

    def cmd_handle_attack(self):
        pass

    def cmd_handle_export(self):
        pass

    def get_cmd(self):
        self.prompt()
        try:
            cmd = raw_input(UiLIb.fmt(UiLIb.PURPLE, ">>>: "))
        except IOError:
            pass
        return cmd

    def get_status(self):
        pass





# ==========================================================
# 单例模式
singleton = Command()