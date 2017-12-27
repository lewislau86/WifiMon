#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : TinyMon.py
Author: Lewis Lau
Date  : 2017/12/12
Desc  : 
"""
from scapy.all import *
from MacParser import singleton as whmp
import datetime
import sys
import errno
from select import select, error as select_error
import subprocess

# Fixes the bug for parsing special characters
reload(sys)
sys.setdefaultencoding( "utf-8" )
#sys.setdefaultencoding('gbk')

class packetParse(object):
    __intf = None
    __Numap = 0
    __Numclients = 0
    __Currentloc = None
    __clients = []
    __macClient = []
    __accessPoints = []
    __macAP = []
    __hideSsidMac = []
    __hideSsidDict = {}


    def get_rssi(self, extra):
        rssi = int(-(256 - ord(extra[-2:-1])));

        if rssi not in xrange(-100, 0):
            rssi = (-(256 - ord(extra[-4:-3])));

        if rssi < -100:
            return -1;
        return rssi;

    def PacketHandler(self , pkt):
        mymac = self.__mac_addr
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
                try:
                    if pkt.haslayer(Dot11ProbeReq):
                        self.PacketProbeReq(pkt)
                    if pkt.haslayer(Dot11Beacon):
                        self.PacketBeacon(pkt)
                    if pkt.haslayer(Dot11ProbeResp):
                        self.PacketProbeResp(pkt)
                except UnicodeDecodeError:
                    pass


    def PacketProbeResp(self, pkt):
        mac = pkt.getlayer(Dot11).addr2
        if mac in self.__hideSsidMac and False==self.__hideSsidDict.has_key(mac):
            ssid = pkt.getlayer(Dot11ProbeResp).info
            # 这里需要一个字典，保存mac：ssid的关系
            self.__hideSsidDict[mac] = ssid



    def PacketProbeReq(self, pkt):
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

        if ssid_probe not in self.__clients and ssid_probe != "":
            self.__clients.append(ssid_probe)
            self.__macClient.append(mac)
            print ('[Client:' + manufacture + '/' + mac + '] [SSID:' + ssid_probe.decode("utf-8") + ']')
            #Verbose.vLogClient(manufacture,mac,ssid_probe.decode("utf-8"))
        elif ssid_probe in self.__clients and mac not in self.__macClient:
            self.__macClient.append(mac)
            print('[Client:' + manufacture +'/' + mac + '] [SSID:' + ssid_probe.decode("utf-8") + ']')
            #Verbose.vLogClient(manufacture, mac, ssid_probe.decode("utf-8"))
            self.__Numclients += 1
        elif mac not in self.__macClient and ssid_probe == "":
            self.__macClient.append(mac)
            print('[Client:' + manufacture + '/' + mac + '] [New Client]')
            #Verbose.vLogClient(manufacture, mac, "New Client")
            self.__Numclients += 1


    def PacketBeacon(self, pkt):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')

        ssid_probe = pkt.info
        manufacture = str(whmp.get_manuf(pkt.addr2))
        mac = pkt.addr2

       # gpsloc = ''

        crypto = self.CryptoInfo(pkt)

       # if self.__args.gpstrack:
       #     gpsloc = str(gpsd.fix.latitude) + ':' + str(gpsd.fix.longitude)

        if ssid_probe not in self.__accessPoints and ssid_probe != "":
            self.__accessPoints.append(ssid_probe)
            self.__macAP.append(mac)
            print('[AP:' + manufacture +'/'+ mac + '] ['+crypto+'] ['+'SSID:'+ssid_probe.decode("utf-8") + ']')
            #Verbose.vLogAP(manufacture , mac,crypto,ssid_probe.decode("utf-8"))
            self.__Numap += 1
        elif ssid_probe in self.__accessPoints and mac not in self.__macAP:
            self.__macAP.append(mac)
            print('[AP:' + manufacture + '/' + mac + '] ['+crypto+'] ['+'SSID:'+ ssid_probe.decode("utf-8") + ']')
            #Verbose.vLogAP(manufacture, mac, crypto, ssid_probe.decode("utf-8"))
            self.__Numap += 1
        elif ssid_probe=="" and mac not in self.__hideSsidMac:
            # 第一次探测到隐藏的ssid，加入列表
            self.__hideSsidMac.append(mac)
        elif ssid_probe=="" and mac in self.__hideSsidMac:
            if self.__hideSsidDict.has_key(mac):
                # 已经在列表里面，且Dot11ProbeResp时已经有了记录
                print ('[Hidden-AP:' + manufacture + '/' + mac + '] [' + crypto + '] \
                                #       [' + 'SSID:' + self.__hideSsidDict[mac] + ']')
                ##UiLIb.CPrint.GREEN('[Hidden-AP:' + manufacture + '/' + mac + '] [' + crypto + '] \
                #       [' + 'SSID:' + self.__hideSsidDict[mac] + ']')

    def do_sniff(self,intf):
        self.__intf == intf
        try:
            print ("****do_sniff****\n")
            sniff(iface=self.__intf, prn=self.PacketHandler, store=0)
        except select_error as exc:
            if exc[0] == errno.EINTR:
                print "I catch it!\r\n"
                #sniff(iface=self.__intf, prn=self.PacketHandler, store=0)
        except Exception, e:
            msg = traceback.format_exc()  # 方式1
            print (msg)


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
            crypto = crypto + " WPS"

        return crypto

    def enableNICMonitorMode(self , nicDev):
        print " Setting Wireless card into Monitor Mode"
        if 'mon' not in nicDev:
            cmd = ['airmon-ng', 'start',nicDev]
            ret, _ = self.runCmd(cmd)
            if 0 == ret:
                return True
            else:
                return False

    def runCmd(self , cmd):
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ret = p.wait()
            if p.returncode == 0:
                return ret, p.stdout.read()
            else:
                return ret, None
        except OSError, e:
            return e.errno, None

    def get_mac(self, intf):
        self.__mac_addr = open('/sys/class/net/%s/address' % intf).read().rstrip()
        return self.__mac_addr


def main():
    inft = "wlan1"
    Packet = packetParse()

    if True == Packet.enableNICMonitorMode(inft):
        Packet.get_mac(inft)
        Packet.do_sniff(inft+"mon")


if __name__ == "__main__":
    main()