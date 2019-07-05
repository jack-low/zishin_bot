#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import json
import time

# pip install ws4py
from ws4py.client.threadedclient import WebSocketClient

USERID = "trialuser"
PASSWORD = "trialpass"
TERMID = "0000000001"
WS_SERVER_URI = "wss://localhost:443"

class EventPushClient(WebSocketClient):
    def opened(self):
        print('EVENT : opened')
        data = {
          "version"   : {
            "common_version"  : "1",
            "details_version" : "1"
          },
          "common"    : {
            "datatype"  : "authentication",
            "msgid"     : "",
            "sendid"    : "",
            "senddatetime": ""
          },
          "details"    : {
            "password": PASSWORD
          },
          "sender"    : {
            "version"   : "1",
            "userid"    : USERID,
            "termid"    : TERMID
          },
          "receiver"  : {
            "version"   : "1",
            "userid"    : "*",
            "termid"    : "*"
          },
        }
        self.senddata(data)

        print

    def closed(self, code, reason):
        print('EVENT : Closed down, code=%s, reason=%s' % (code, reason))
        print

    def received_message(self, m):
        print('EVENT : receive')
        message = json.loads(m.data)
        print('datatypename: %s' % message["common"]["datatype"])
        print(message)
        print

    def senddata(self, data):
        message = json.dumps(data)
        self.send(message)
        print("senddata:")
        print(message)
        print

if __name__ == '__main__':
    try:
        argvs = sys.argv
        argc = len(argvs)
        connections = []

        if argc == 1:
          num = 1
        else:
          num = int(argvs[1])

        print(num)
        for i in range(num):
          ws = EventPushClient(WS_SERVER_URI,
                               protocols=['http-only', 'chat'])
          ws.connect()
          connections.append(ws)

        while( 1 ):
          time.sleep(1)
    except KeyboardInterrupt:
        print('')
        for wsc in connections:
          wsc.close()
        sys.exit(1)
    except:
        print('EXCEPT : %s' % sys.exc_info()[1])
        ws.close()
        sys.exit(1)

    print('success. exit.')
    sys.exit(0)