#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''

=================================
=================================
=========Author:Task138==========
========Power By Python3=========
=================================
=================================


'''
import json, requests, warnings

warnings.filterwarnings('ignore')

def keepAlive(cookie, signInstanceWid):
    headers = {
        'Host': '这里填写抓包得到的学校域名',
        'Content-Type': 'application/json',
        'Cookie': cookie,
        'Accept': '*/*',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 (4833404928)cpdaily/8.2.1  wisedu/8.2.1',
        'Connection': 'keep-alive',
        'Origin': '这里填写抓包得到的学校域名'
    }

    url = '这里填写获取表单详情信息的URL'

    body = {
        'signInstanceWid': signInstanceWid,
        "signWid":"466705"
    }

    data = json.dumps(body)

    req = requests.post(url=url, data=data, verify=False, headers=headers)
    response = json.loads(req.text)

    status = response['message']
    print(status)
    return status

if __name__ == '__main__':
    with open('test.json', 'r') as fp2:
        accounts = json.load(fp2)
        fp2.close()
    for k, v in accounts.items():
        with open('Wid.json', 'r') as fp:
            data = json.load(fp)
            fp.close()

        signInstanceWid = data['signInstanceWid']
        cookie = v['cookie']

        status = keepAlive(cookie, signInstanceWid)
        if status == 'SUCCESS':
            print('[ %s ] 保活成功' % k)
        else:
            print('[ %s ] 保活失败' % k)
