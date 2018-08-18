import urllib.request
import urllib.parse
import base64
import time
import uuid
import hashlib
import json
import logging
import tkinter.messagebox

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s Process%(process)d:%(thread)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='../logs/OcrApi.log',
                    filemode='a')


def query_api(data):
    global text, result_list
    result_list = []
    nonce_str = str(uuid.uuid4()).replace('-', '')
    data = base64.b64encode(data)
    app_id = 2107761575
    app_key = '2qmvi0sY5vRb3PAO'
    temp = [('app_id', app_id), ('time_stamp', int(time.time())), ('nonce_str', nonce_str),
            ('image', data)]
    temp.sort()
    temp.append(('app_key', app_key))
    temp = dict(temp)
    temp_str = urllib.parse.urlencode(temp)
    md5_str = hashlib.md5(temp_str.encode('UTF-8')).hexdigest().upper()
    del temp['app_key']
    temp['sign'] = md5_str
    data = urllib.parse.urlencode(temp).encode('UTF-8')
    logging.debug('Request----->' + str(temp))
    request = urllib.request.Request(r'https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr', data)
    response = urllib.request.urlopen(request)
    result = response.read().decode('utf-8')
    temp = json.loads(result)
    logging.debug('Response----->' + str(temp))
    if temp['ret'] != 0:
        print('错误！可能是截图出错或者响应时间超过五秒。')
        tkinter.messagebox.showerror('错误', '可能是截图出错或者响应时间超过五秒')
    else:
        text = ''
        for item in temp['data']['item_list']:
            result_map = []
            result_map = dict(result_map)
            result_map['itemstring'] = item['itemstring']
            result_map['itemcoord'] = item['itemcoord']
            text += item['itemstring']
            result_list.append(result_map)
    print(text)
    return result_list
