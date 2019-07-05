#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import urllib2
import codecs
import datetime

import json

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

# 接続先URL ローカル
BASE_URL = 'https://api-w01.pf.iij-engineering.co.jp/info/1.0/data/get.json'
# Header
HEADERS = {
    'Content-Type': 'application/json'
}

def testcall(method):
    """
    testcall
    """
    try:
        # url
        url = '%s%s' % (BASE_URL, method)

        # param
        param = {
            'system' : {
                'login_name' : 'trialuser',   # 認証ユーザ名
                'login_pass' : 'trialpass',   # 認証パスワード
                'app_servername' : '',        # APIの呼び出し元システムのサーバ名
                'app_username' : '',          # APIの呼び出し元システムのログイン名
                'timezone' : '',              # タイムゾーン変換　※現時点では"Asia/Tokyo"のみ対応
                'use_rawdata' : '0',          # 生データ利用有無
            },
            'query' : {
                'idlist' : ['12', '13',],     # idの配列
                'datatypename' : 'trialinfo', # データタイプ名
                'dataversion' : 1,            # データバージョン
            }
        }

        # jsonに変換します
        data = json.dumps(param)

        # header
        HEADERS['Content-Length'] = len(data)

        print
        print 'request:'
        print HEADERS
        print data
        print

        # サーバにリクエストします
        response = _request(url, data, HEADERS)
        print 'response:'
        print response
        print

        # 結果を表示します
        print 'result:'
        print_response(response)
        print
    except:
        msg = 'except ; %s; %s' % (sys.exc_info()[0], sys.exc_info()[1])
        print(msg)

    return 0

def _request(url, data, headers={}):
    """
    リクエストします
    """
    req = urllib2.Request(url, data, headers)
    f = urllib2.urlopen(req)
    res_body = f.read()
    f.close()

    return res_body

def print_response(response):
    """
    結果を見やすくします
    """
    # jsonを辞書に変換します
    response = json.loads(response)

    print 'code = %s' % response['code']
    print 'message = %s' % response['message']

    if 'datalist' in response:
        print 'datalist = '
        print '------------'

        for item in response['datalist']:
            for k, v in item.iteritems():
                print '%s : %s' % (k, v)

            print '------------'

if __name__ == '__main__':
    retcode = 0

    print('=============================')

    testcall('/data/get.json')

    print('=============================')

    sys.exit(retcode)