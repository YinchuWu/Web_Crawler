# -*- coding:utf-8 -*-
import md5
import os
import requests
import json
import time
import sys
import unittest
from qiniu import Auth, put_file, etag, urlsafe_base64_encode


IQFA_ACCESS_KEY = "9aPx3h888D0rWcX20HSayvHqxlvxHbjn"
IQFA_SECRET_KEY = "CNkx6KJYxTtEr6WF3ChOEKZIl4WMWG4n0i3Hvo8Ov4o"

IQFA_PIC_DOMAIN = "http://otl6ypoog.bkt.clouddn.com"
IQFA_IP_ADDRESS = "47.94.71.29"
IQFA_SUPPORT_PROTOCOL = "http://"
IQFA_REQUEST_PATH = "/api/image/token"
#IQFA_REQUEST_PATH = "/api/video/token"


def sign(secret_key, params=None):
    if params:
        params = sorted(params)
        sign_string = secret_key
        for i in params:
            key, value = i
            sign_string += str(key)
            sign_string += str(value)
        sign_string += secret_key

        hash_string = md5.new()
        hash_string.update(sign_string)
        return hash_string.hexdigest().upper()
    else:
        pass


def requestWithFileName(file_name):
    time_stamp = int(time.time())
    params = [
        ("ACCESS_KEY", IQFA_ACCESS_KEY),
        ("TIMESTAMP", time_stamp),
        ("file_name", file_name)
    ]
    sign_string = sign(IQFA_SECRET_KEY, params)
    data = {
        "ACCESS_KEY": IQFA_ACCESS_KEY,
        "SIGN_KEY": sign_string,
        "TIMESTAMP": time_stamp,
        "file_name": file_name
    }
    resp = requests.post(IQFA_SUPPORT_PROTOCOL +
                         IQFA_IP_ADDRESS + IQFA_REQUEST_PATH, data=data)
    return resp.text


if __name__ == '__main__':
    f = open('url_list.txt', 'w')
    for i in range(10):  # 10 attemps in default
        print 'Creating image url instance {}.'.format(i)
        res = requestWithFileName("Scra_test" + str(i) + ".jpg")
        a = "Res: {}".format(res)
        token = (json.loads(res)['token'])
        path = (json.loads(res)['path'])

        # local file directory
        loaclfile = 'Raw_images/' + sys.argv[1]
        ret, info = put_file(token, path, loaclfile)

        if info.status_code == 200:
            a = "Success Upload Qiniu: {}".format(loaclfile)
            a = os.path.join('http://otl6ypoog.bkt.clouddn.com', path)
            f.write(a + ' ')
        else:
            print "Upload Qiniu Failure !"
    f.close()
