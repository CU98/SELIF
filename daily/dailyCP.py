
#!/usr/bin/evn python
#-*- coding:utf-8 -*-

'''
==========================
=====POWER BY python3=====
==========================
'''

import requests, json, warnings, datetime

warnings.filterwarnings('ignore')

def getData(cookie, signInstanceWid):

    # 时段判断
    # 当前时段
    now_hour = datetime.datetime.now().hour

    # 签到时段
    # 早：9
    # 中：14
    # 晚：23
    sign_hour = 0
    if now_hour < 9:
        sign_hour = 7
    elif now_hour < 14:
        sign_hour = 12
    else:
        sign_hour = 23

    print(now_hour, sign_hour)
    if sign_hour == 7:
        signWid = '466705'
    elif sign_hour == 12:
        signWid = '466703'
    else:
        signWid = '466708'
    print(signInstanceWid, signWid)

    info = {}

    info['signInstanceWid'] = signInstanceWid

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
        'signWid': signWid
    }

    data = json.dumps(body)

    req = requests.post(url=url, data=data, verify=False, headers=headers)

    thread = 200
    for i in range(thread + 1):
        body = {
            'signInstanceWid': str(int(signInstanceWid) + i),
            'signWid': signWid
        }
        data = json.dumps(body)
        req = requests.post(url=url, data=data, verify=False, headers=headers)
        response = json.loads(req.text)
        now = datetime.datetime.today()
        current_date = now.strftime('%Y-%m-%d')

        try:
            senderUserName = response['datas']['senderUserName']
            sign_date = response['datas']['rateSignDate']
            rateTaskBeginTime = response['datas']['rateTaskBeginTime']
            print(rateTaskBeginTime, body['signInstanceWid'])
        except:
            print(body)
            continue

        if ('这里填写辅导员的名字' in senderUserName) and (current_date in sign_date):
            if signWid == '466705':
                # 早上签到
                if rateTaskBeginTime != '07:00':
                    continue
            if signWid == '466703':
                # 中午签到
                if rateTaskBeginTime != '12:00':
                    continue
            if signWid == '466708':
                # 晚上签到
                if rateTaskBeginTime != '22:00':
                    continue

            new_signInstanceWid = response['datas']['signInstanceWid']
            try:
                wid = response['datas']['extraField'][0]['extraFieldItems'][0]['wid']
            except:
                wid = 58679
            info['signInstanceWid'] = new_signInstanceWid
            info['wid'] = wid

            if new_signInstanceWid != signInstanceWid:
                with open('Wid.json', 'w') as fp3:
                    new_data = '{"signInstanceWid":"%s"}' % (new_signInstanceWid)
                    fp3.write(new_data)
                    fp3.close()
                    print('更新成功，当前数值：')
                    print('signInstanceWid [ %s ]' % new_signInstanceWid)
            break
        else:
            print(senderUserName)
    return info

def submitForm(cookie, info, username):

    headers = {
        'Host': '这里填写抓包得到的学校域名',
        'Content-Type': 'application/json',
        'Cpdaily-Extension': '7Q881vmOiX7oHMgy2uiNNl8ZFV6TrEm+YxKkdJOzmMMGgT2eTPPHxBxY02LK 4Qq42SCAuunYl3r52lBcvtJAKSbT6h1n94BA3spnuAfnh7YCJbOJpAxjn9mx X8a8G9i9OYPNioL6UB76/x7ZeuZly9Ai1L6sAFWwtkczAcTdTSKdx+aqI5XO xPbqJrAztcBx+CtvFlsMsGcI2uKHLD3I2sgoFB4XoYhFv/4SjuWX+N/W24Oy oF8txhaTS1PJhmetIYLybnMWyAoiH6lmwknAMjSJdtqLe51u',
        'Cookie': cookie,
        'Accept': '*/*',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': '%E4%BB%8A%E6%97%A5%E6%A0%A1%E5%9B%AD/1 CFNetwork/1128.0.1 Darwin/19.6.0',
        'Connection': 'keep-alive'
    }

    url = '这里填写post提交表单的URL'
    body = {
        "signInstanceWid": info['signInstanceWid'],
        "longitude": 这里填写抓包抓取到的经度,
        "latitude": 这里填写抓包抓取到的维度,
        "isMalposition": 0,
        "abnormalReason": "",
        "signPhotoUrl": "",
        "position": "这里填写定位的地址信息",
        "isNeedExtra": 1,
        "extraFieldItems": [{
            "extraFieldItemValue": "小于37.3℃",
            "extraFieldItemWid": info['wid']
        }]
    }

    data = json.dumps(body)

    req = requests.post(url=url, headers=headers, data=data, verify=False)
    response = req.text
    print(response)

    if "SUCCESS" in response:
        print('[ %s ]签到成功' % username)
        return True
    elif "该收集已填写无需再次填写" in response:
        print('[ %s ]签到成功' % username)
        return True
    elif "该收集已结束！" in response:
        print('[ %s ]签到成功' % username)
        return True
    elif "该签到已截止！" in response:
        print('[ %s ]签到成功' % username)
        return True
    else:
        print('[ %s ]签到失败' % username)
        return False




if __name__ == '__main__':
    success = 0
    failed = 0
    failed_data = []

    with open('test.json', 'r') as fp2:
        accounts = json.load(fp2)
        fp2.close()
    for k, v in accounts.items():
        with open('Wid.json', 'r') as fp:
            data = json.load(fp)
            fp.close()

        signInstanceWid = data['signInstanceWid']
        address = v['address']
        cookie = v['cookie']

        info = getData(cookie, signInstanceWid)
        submitForm(cookie, info, k)
