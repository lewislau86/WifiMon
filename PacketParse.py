#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : PacketParse.py
Author: Lewis Lau
Date  : 2017/11/16
Desc  : 
"""
from scapy.all import *

class packetParse(object):
    def PacketHandler(pkt):
        mymac = getmac(intf)
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
                    PrintPacketClient(pkt)
                if args.access:
                    if pkt.type == PROBE_REQUEST_TYPE and pkt.subtype == AP_BROADCAST_SUBTYPE:
                        PrintPacketAP(pkt)

    def do_sniff():
        try:
            sniff(iface=intf, prn=PacketHandler, store=0)
        except Exception, e:
            print 'Caught exception while running sniff()', e



singleton = packetParse()