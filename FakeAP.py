#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : FakeAP.py
Author: Lewis Lau
Date  : 2017/12/27
Desc  : 
"""

from Utils import singleton as Utils
from Verbose import singleton as Verbose

#from PraseArg import singleton as PraseArg

conf = "interface=wlan0\n" \
       "driver=nl80211\n" \
       "ssid={0}\n" \
       "hw_mode=g\n" \
       "channel=6\n" \
       "wmm_enabled=1\n" \
       "macaddr_acl=0\n" \
       "auth_algs=1\n" \
       "ignore_broadcast_ssid=0\n" \
       "wpa=2\n" \
       "wpa_passphrase={1}\n" \
       "wpa_key_mgmt=WPA-PSK\n" \
       "rsn_pairwise=CCMP\n"

class FakeAP(object):
    def runIptableRuleInit(self):
        '''
        iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
        iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
        iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
        '''
        Utils.runCmd("iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
        Utils.runCmd("iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT")
        Utils.runCmd("iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT")

    def runHostapd(self):
        '''
        hostapd /etc/hostapd/hostapd.conf
        '''
        Utils.runCmd("hostapd /etc/hostapd/hostapd.conf")

    def runUdhcpd(self):
        '''
        udhcpd -f /etc/udhcpd.conf
        '''
        Utils.runCmd("udhcpd -f /etc/udhcpd.conf")

    def setHostapdConf(self,ssid,pwd):
        confstr  = conf.format(ssid,pwd)
        f = open('/Users/Lewis/etc/hostapd/hostapd.conf', 'w')
        f.write(confstr)
        f.close()

    def getPwdbySSID(self,ssid):
        for apInfo in Verbose.__ApInfo:
            if apInfo['ssid'] == ssid:
                mac = apInfo['mac']
        # 查询密码
        return ssid+"123"

    def runFakeWifi(self,ssid,pwd):
        self.setHostapdConf(ssid,pwd)
        self.runIptableRuleInit()
        self.runUdhcpd()
        self.runHostapd()

    def fakeWifi(self,ssid):
        print("*DEBUG*\t\t fake Wifi running")
        pwd = self.getPwdbySSID(ssid)
        print("*DEBUG*\t\t pwd:"+pwd)
        self.runFakeWifi(ssid,pwd)
# ==========================================================
# 单例模式
singleton = FakeAP()
#__args = PraseArg.get_parse()
#print(__args.fake)