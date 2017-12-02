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
#from gps import *
from MacParser import singleton as whmp
import datetime
import logging
import Frame80211

#PROBE_REQUEST_TYPE=0
#PROBE_REQUEST_SUBTYPE=4
AP_BROADCAST_SUBTYPE=8


class packetParse(object):
    __intf = None
    __Numap = None
    __Numclients = 0
    __Currentloc = None
    __args = ()
    __clients = []
    __macClient = []
    __accessPoints = []
    __macAP = []

    def __init__(self):
        self.__args = PraseArg.get_parse()

    def get_rssi(self, extra):
        rssi = int(-(256 - ord(extra[-2:-1])));

        if rssi not in xrange(-100, 0):
            rssi = (-(256 - ord(extra[-4:-3])));

        if rssi < -100:
            return -1;
        return rssi;

    def PacketHandler(self , pkt):
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
                #if pkt.type == Frame80211.Type.Management and pkt.subtype == PROBE_REQUEST_SUBTYPE:
                 if pkt.type == Frame80211.Type.Management  and pkt.subtype == Frame80211.Management.ProbeReq:
                    self.PrintPacketClient(pkt)
                #if self.__args.access:
                #if pkt.type == Frame80211.Type.Management and pkt.subtype == AP_BROADCAST_SUBTYPE:
                    if pkt.type == Frame80211.Type.Management and pkt.subtype == Frame80211.Management.Beacon:
                        self.PrintPacketAP(pkt)


    def PrintPacketClient(self , pkt):
        '''

        '''
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')

        ssid_probe = pkt.getlayer(Dot11ProbeReq).info
        manufacture = str(whmp.get_manuf(pkt.addr2))
        mac = pkt.addr2
        gpsloc = ''
        crypto = 'None'  # instead of being blank, client has none for crypto probe request

       # if self.__args.gpstrack:
       #     gpsloc = str(gpsd.fix.latitude) + ':' + str(gpsd.fix.longitude)

        # Logging info
        fields = []
        fields.append(st)  # Log Time
        fields.append('Client')  # Log Client or AP
        fields.append(mac)  # Log Mac Address
        fields.append(manufacture)  # Log Device Manufacture
        fields.append(ssid_probe.decode("utf-8"))  # Log SSID
        fields.append(crypto)  # Log SSID
        #fields.append(gpsloc)  # Log GPS data
        #fields.append(args.location)  # Log GPS data
        fields.append(str(self.get_rssi(pkt.notdecoded)))  # RSSI

        # if ssid is not in clients and its not empty then print out, add ssid and mac to lists
        if ssid_probe not in self.__clients and ssid_probe != "":
            self.__clients.append(ssid_probe)
            self.__macClient.append(mac)
           # print W + '[' + R + 'Client' + W + ':' + C + manufacture + W + '/' + B + mac + W + '] [' + G + 'SSID' + W + ': ' + O + ssid_probe.decode(
           #     "utf-8") + W + ']'
            print '[Client:' + manufacture + '/' + mac + '] [' + 'SSID' + ': ' + ssid_probe.decode("utf-8") + ']'
        # if ssid is in clients but mac isnt seen before then print out and add the mac to the list
        elif ssid_probe in self.__clients and mac not in self.__macClient:
            self.__macClient.append(mac)
            #print W + '[' + R + 'Client' + W + ':' + C + manufacture + W + '/' + B + mac + W + '] [' + G + 'SSID' + W + ': ' + O + ssid_probe.decode(
            #    "utf-8") + W + ']'
            print '[Client:' + manufacture +'/' + mac + '] [SSID: ' + ssid_probe.decode("utf-8") + ']'
            self.__Numclients += 1
        # if mac is not in the list and the probe has a broadcast (empty) then add mac to list
        elif mac not in self.__macClient and ssid_probe == "":
            self.__macClient.append(mac)
            #print W + '[' + R + 'Client' + W + ':' + C + manufacture + W + '/' + B + mac + W + ']' + W + ' New Client'
            self.__Numclients += 1

        #logger.info(self.__args.delimiter.join(fields))

    def PrintPacketAP(self , pkt):

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')

        ssid_probe = pkt.info
        manufacture = str(whmp.get_manuf(pkt.addr2))
        mac = pkt.addr2

       # gpsloc = ''

        crypto = self.CryptoInfo(pkt)

       # if self.__args.gpstrack:
       #     gpsloc = str(gpsd.fix.latitude) + ':' + str(gpsd.fix.longitude)

        # Logging info
        fields = []
        fields.append(st)  # Log Time
        fields.append('AP')  # Log Client or AP
        fields.append(mac)  # Log Mac Address
        fields.append(manufacture)  # Log Device Manufacture
        fields.append(ssid_probe.decode("utf-8"))  # Log SSID
        fields.append(crypto)  # Log SSID
       # fields.append(gpsloc)  # Log GPS data
       # fields.append(args.location)  # Log GPS data
        fields.append(str(self.get_rssi(pkt.notdecoded)))  # RSSI

        # if AP ssid is not in clients and its not empty then print out, add  AP ssid and mac to lists
        if ssid_probe not in self.__accessPoints and ssid_probe != "":
            self.__accessPoints.append(ssid_probe)
            self.__macAP.append(mac)
            #print W + '[' + R + 'AP' + W + ':' + C + manufacture + W + '/' + B + mac + W + '] [' + T + crypto + W + '] [' + G + 'SSID' + W + ': ' + O + ssid_probe.decode(
            #    "utf-8") + W + ']'
            print('[AP:' + manufacture +'/'+ mac + '] ['+crypto+'] ['+'SSID:'+ssid_probe.decode("utf-8"))
            self.__Numap += 1
        # if ssid is in clients but mac isnt seen before then print out and add the mac to the list
        elif ssid_probe in accessPoints and mac not in self.__macAP:
            macAP.append(mac)
            #print W + '[' + R + 'AP' + W + ':' + C + manufacture + W + '/' + B + mac + W + '] [' + T + crypto + W + '] [' + G + 'SSID' + W + ': ' + O + ssid_probe.decode(
            #    "utf-8") + W + ']'
            self.__Numap += 1

        logger.info(self.__args.delimiter.join(fields))

    def do_sniff(self , intf):
        self.__intf = intf
        try:
            sniff(iface=self.__intf, prn=self.PacketHandler, store=0)
        except Exception, e:
            msg = traceback.format_exc()  # 方式1
            print (msg)
        print 'Caught exception while running sniff()', e

    def CryptoInfo(self , pkt):
        p = pkt[Dot11Elt]
        cap = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
                          "{Dot11ProbeResp:%Dot11ProbeResp.cap%}").split('+')
        crypto = ""
        while isinstance(p, Dot11Elt):
            if p.ID == 48:
                crypto = "WPA2"
            elif p.ID == 221 and p.info.startswith('\x00P\xf2\x01\x01\x00'):
                crypto = "WPA"
            p = p.payload
        if not crypto:
            if 'privacy' in cap:
                crypto = "WEP"
            else:
                crypto = "OPN"
        if "0050f204104a000110104400010210" in str(pkt).encode("hex"):
            crypto = crypto + R + " WPS"

        return crypto



singleton = packetParse()