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
        #Utils.runCmdShell("/sbin/iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
        #Utils.runCmdShell("/sbin/iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT")
        #Utils.runCmdShell("/sbin/iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT")
        Utils.runSystem("/sbin/iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
        Utils.runSystem("/sbin/iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT")
        Utils.runSystem("/sbin/iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT")

    def runHostapd(self):
        '''
        hostapd /etc/hostapd/hostapd.conf
        '''
        print("runHostapd")
        #ret,err = Utils.runCmdShell("hostapd /etc/hostapd/hostapd.conf")
        Utils.runSystem("hostapd /etc/hostapd/hostapd.conf &")


    def runUdhcpd(self):
        '''
        udhcpd -f /etc/udhcpd.conf
        '''
        print("runUdhcpd")
        Utils.runCmdShell("udhcpd -f /etc/udhcpd.conf &")

    def setHostapdConf(self,ssid,pwd):
        confstr  = conf.format(ssid+"_fake",pwd)
        f = open('/etc/hostapd/hostapd.conf', 'w')
        f.write(confstr)
        f.close()

    def getPwdbySSID(self,ssid):
        __apInfo = Verbose.get_apInfo()
        for apInfo in __apInfo:
            if apInfo['ssid'] == ssid:
                mac = apInfo['mac']
        # 查询密码
        return "12345678"

    def getEncryptionMethodbySSID(self,ssid):
        __apInfo = Verbose.get_apInfo()
        for apInfo in __apInfo:
            if apInfo['ssid'] == ssid:
                method = apInfo['crypto']
        return method

    def getMacbySSID(self,ssid):
        __apInfo = Verbose.get_apInfo()
        for apInfo in __apInfo:
            if apInfo['ssid'] == ssid:
                mac = apInfo['mac']
        return mac

    def setMacAddr(self,mac):
        # /sbin/ifconfig
        #Utils.runCmdShell("/sbin/ifconfig wlan0 down")
        #Utils.runCmdShell("/sbin/ifconfig wlan0 hw ether " + mac)
        #Utils.runCmdShell("/sbin/ifconfig wlan0 up")
        Utils.runSystem("/sbin/ifconfig wlan0 down")
        Utils.runSystem("/sbin/ifconfig wlan0 hw ether " + mac )
        Utils.runSystem("/sbin/ifconfig wlan0 up")


    def resetWlan0(self):
        #Utils.runCmdShell("/sbin/ifconfig wlan0 down")
        #Utils.runCmdShell("/sbin/ifconfig wlan0 up")
        Utils.runSystem("/sbin/ifconfig wlan0 down")
        Utils.runSystem("/sbin/ifconfig wlan0 up")

    def runFakeWifi(self,ssid,pwd,mac):
        self.setMacAddr(mac)
        self.setHostapdConf(ssid,pwd)
        self.runIptableRuleInit()
        self.runHostapd()
        self.resetWlan0()
        self.runUdhcpd()

    def convertEncryptionName(self,name):
        oname = "wep"
        if name == "WPA2":
            oname = "psk2"
        return oname

    def fackWifiWithParameter(self,index,ssid,mac,encryptMethod,key):
        Utils.runSystem("/sbin/uci set wireless.@wifi-iface["+index+"].ssid="+ssid)
        Utils.runSystem("/sbin/uci set wireless.@wifi-iface["+index+"].macaddr="+mac)
        if len(encryptMethod) == 0 or len(key) == 0:
             Utils.runSystem("/sbin/uci delete wireless.@wifi-iface["+index+"].encryption")
             Utils.runSystem("/sbin/uci delete wireless.@wifi-iface["+index+"].key")
        else:
            Utils.runSystem("/sbin/uci set wireless.@wifi-iface["+index+"].encryption="+encryptMethod)
            Utils.runSystem("/sbin/uci set wireless.@wifi-iface["+index+"].key="+key)
        Utils.runSystem("/sbin/uci commit")
        Utils.runSystem("/sbin/wifi")

    def fakeWifi(self,ssid,index):
        print("*DEBUG*\t\t fake Wifi running")
        pwd = self.getPwdbySSID(ssid)
        mac = self.getMacbySSID(ssid)
        method = self.getEncryptionMethodbySSID(ssid)
        print("fackWifiWithParameter key:"+pwd+" mac:"+mac + " method:" +method)
        if method == "OPN":
            self.fackWifiWithParameter(index,ssid,mac,"","")
        else:
            name = self.convertEncryptionName(method)
            self.fackWifiWithParameter(index,ssid,mac,name,pwd)
        print("*DEBUG*\t\t pwd:"+pwd)


# ==========================================================
# 单例模式
singleton = FakeAP()
#__args = PraseArg.get_parse()
#print(__args.fake)