#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File  : Frame80211.py
Author: Lewis Lau
Date  : 2017/11/30
Desc  :  0b   开头表示二进制
"""
'''
Management frames(管理帧: Type=00)【注 a】
【注 a】管理帧之 subtype 值 0110-0111 与 1110-1111 目前保留尚未使用
0000 Association request(连接要求)
0001 Association response(连接应答)
0010 Reassociation request(重新连接要求)
0011 Reassociation response(重新连接应答)
0100 Probe request(探查要求)
0101 Probe response(探查应答)
1000 Beacon(导引信号)
1001 Announcement traffic indication message (ATIM)(数据代传指示通知信号)
1010 Disassociation(解除连接)
1011 Authentication(身份验证)
1100 Deauthentication(解除认证) Control frames(控制帧:


Control frames(控制帧 Type=01)【注 b】
【注 b】控制帧之 subtype 值 0000-0111 目前保留尚未使用
1010    Power Save-Poll(省电模式-轮询)
1011    RTS(请求发送)
1100    CTS(允许发送)
1101    ACK(应答)
1110    CF-End(免竞争期间结束)
1111    CF-End(免竞争期间结束)+CF-Ack(免竞争期间 回应)

Data frames (数据帧:Type=10) 【注 c】
【注 c】由 802.11e 任务小组所提议,但尚未标准化。注意这些帧均为 1 开头，
0000    Data(数据)
0001    Data+CF-Ack
0010    Data+CF-Poll
0011    Data+CF-Ack+CF-Poll
0100    Null data (无数据:未发送数据) 
0101    CF-Ack (未发送数据)
0110    CF-Poll (未发送数据) 
0111    Data+CF-Ack+CF-Poll
1000    QoS Data【注 c】
1001    QoS Data + CF-Ack【注 c】
1010    QoS Data + CF-Poll【注 c】
1011    QoS Data + CF-Ack + CF-Pol【注 c】 
1100    QoS Null (未发送数据)【注 c】
1101    QoS CF-Ack (未发送数据) 【注 c】
1110    QoS CF-Poll (未发送数据) 【注 c】
1111    QoS CF-Ack+CF-Poll (未发送数据) 【注 c】
'''


Type = {
    'Management':   0b00,
    'Control':      0b01,
    'Data':         0b10
}

Management = {
    'AssReq':       0b0000,
    'AssResp':      0b0001,
    'ReassReq':     0b0010,
    'ReassResp':    0b0011,
    'ProbeReq':     0b0100,
    'ProbeResp':    0b0101,
    'Beacon':       0b1000,
    'ATIM':         0b1001,
    'DisAss':       0b1010,
    'Deauth':       0b1100
}

Control = {
    'PowerSave':    0b1010,
    'RTS':          0b1011,
    'CTS':          0b1100,
    'ACK':          0b1101,
    'CF-End':       0b1110,
    'CF-End+CF-Ack': 0b1111
}

Data = {
    'Data':             0b0000,
    'Data+CF-Ack':      0b0001,
    'Data+CF-Poll':     0b0010,
    'Data+CF-Ack+CF-Poll': 0b0011,
    'NullData':         0b0100,
    'CF-Ack':           0b0101,
    'CF-Poll':          0b0110,
    'Data+CF-Ack+CF-Poll2': 0b0111
}