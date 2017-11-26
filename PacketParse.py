#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : PacketParse.py
Author: Lewis Lau
Date  : 2017/11/16
Desc  : 
"""
from scapy.all import *
from Utils import singleton as Utils
from PraseArg import singleton as PraseArg
from MacParser import singleton as MacParser


PROBE_REQUEST_TYPE=0
PROBE_REQUEST_SUBTYPE=4
AP_BROADCAST_SUBTYPE=8


class packetParse(object):
    __intf = None

    def PacketHandler(self , pkt):
        args = PraseArg.get_parse()
        mymac = Utils.get_mac(self.__intf)
        noise = {
            'ff:ff:ff:ff:ff:ff',  # broadcast
            '00:00:00:00:00:00',  # broadcast
            '33:33:00:',  # ipv6 multicast
            '33:33:ff:',  # spanning tree
            '01:80:c2:00:00:00',  # multicast
            '01:00:5e:',  # broadcast
            'None',
            mymac
        }
        if pkt.haslayer(Dot11):
            if pkt.addr2 not in noise:
                if pkt.type == PROBE_REQUEST_TYPE and pkt.subtype == PROBE_REQUEST_SUBTYPE:
                    self.PrintPacketClient(pkt)
                if args.access:
                    if pkt.type == PROBE_REQUEST_TYPE and pkt.subtype == AP_BROADCAST_SUBTYPE:
                        self.PrintPacketAP(pkt)

    def PrintPacketClient(self , pkt):
        print "PrintPacketClient"
        pass

    def PrintPacketAP(self,pkt):
        print "PrintPacketAP"
        manufacture = str(MacParser.get_manuf(pkt.addr2))
        pass

    def do_sniff(self , intf):
        self.__intf = intf
        print  intf
        try:
            sniff(iface=self.__intf, prn=self.PacketHandler, store=0)
        except Exception, e:
            print 'Caught exception while running sniff()', e



singleton = packetParse()