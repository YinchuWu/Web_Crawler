from urllib import request
from random import randint
import time
from urllib.error import URLError
import requests
import os
import re
import numpy as np
import shutil
import sys

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
     (KHTML, like Gecko) Element Browser 5.0',
               'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
               'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
               'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
     Version/6.0 Mobile/10A5355d Safari/8536.25',
               'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
     Chrome/28.0.1468.0 Safari/537.36',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36']


def get_url(img_link):  # from img_link get search result url
    # proxies = {
    #     'http': '118.190.95.43:9001',
    #     'https': '218.106.205.145:8080'
    # }
    time.sleep(0.5)
    try:
        a = time.time()
        req = requests.get('http://www.pailitao.com/image',
                           params={'q': img_link})
        print('Server response time : %f in get_url process.' %
              (time.time() - a))
        return req.url
    except:
        print('Fail in getting search result url with link : %s!' % img_link)
        return 0


def get_html(obj, url):
    time.sleep(0.5)  # from url get html file, save in obj.txt
    a = time.time()
    req = request.Request(url)
    index = randint(0, 10)
    user_agent = user_agents[index]
    req.add_header('User-agent', user_agent)
    f = open(obj + '.txt', 'wb')
    try:
        response = request.urlopen(req)
        html = response.read()
        f.write(html)
        f.close()
        print('Server response time : %f in get_html process.' %
              (time.time() - a))
        return 1
    except:
        print('Fail to fetch html_file from obj : %s !' % (obj))
        f.close()
        return 0
    # except URLError as e:
    #     print(e.reason)


def fetch_reslut(obj):
    time.sleep(0.1)
    a = time.time()
    f = open(obj + '.txt', 'rb')
    os.mkdir(obj)
    flag = 0
    for line in f.readlines():
        try:
            line = line.decode('utf-8')
        except:
            continue
        # print(line)
        tmp = fetch_image(obj, line)
        if tmp:
            flag = 1
    if flag == 0:
        print('Login process was required!  =. =|||')
        print("Or you'd better make sure your images is corresponding to Ali's DB ")
        return 0
    print('Images fetch time total: %f.' % (time.time() - a))
    return 1


def fetch_image(obj, html):
    s = re.findall(r'"pic_url":"[^,]+"', html)
    # print(s)
    flag = 0
    for i in range(0, len(s)):
        s[i] = s[i][11:-1]
        if s[i][0] == '/':
            s[i] = 'http:' + s[i]
            # print(s[i])
        file_ob = open(obj + '/' + str(i) + ".jpg", 'wb')
        try:
            req_page = request.urlopen(s[i]).read()
            time.sleep(0.01)
            file_ob.write(req_page)
            flag = 1
        except:
            print(
                'Fail to fetch image_file with num : %d from obj : %s !' % (i, obj))
        file_ob.close()
    return flag


def scrapy(img_link, di):
    time.sleep(10)
    # f = open('link.txt')
    # link_set = f.read()
    # link_set = link_set.split(' ')
    url = get_url(img_link)

    get_html(di, url)
    # sacrified = ['Dataset/sacrified' + str(i) for i in range(1)]
    # print(sacrified)
    flag = fetch_reslut(di)
    # while (not flag):
    #     time.sleep(0.5)
    #     # sed = np.random.random_integers(0, 53, 1)
    #     # for i in range(1):
    #     #     time.sleep(0.1)
    #     #     # print(link_set[sed[i]])
    #     #     img_link = link_set[sed[i]]
    #     #     url_tmp = get_url(img_link)
    #     #     # try:
    #     #     #     shutil.rmtree(sacrified[i])
    #     #     # except:
    #     #     #     pass
    #     #     get_html(sacrified[i], url_tmp)
    #     #     print('Surprise motherfucker!!')
    #     #     time.sleep(0.5)
    #     try:
    #         shutil.rmtree(obj)
    #     except:
    #         pass
    #     flag = fetch_reslut(obj)
    return flag


if __name__ == '__main__':
    f = open('url_list.txt')
    url_list = f.read().split(' ')
    for url in url_list:
        try:
            shutil.rmtree('Fetched_images/' + sys.argv[1][:-4])
        except:
            pass
        flag = scrapy(url, 'Fetched_images/' + sys.argv[1][:-4])
        if flag == 1:
            print('Fetch images succeed!')
            os.remove('Fetched_images/' + sys.argv[1][:-4] + '.txt')
            os.remove('url_list.txt')
            break
        print('Waitting for another url instance attemps.')
    if flag == 0:
        print('Oh shit! Rerun command maybe a better choice.')
    f.close()

# get_html('snacks2', 'http://www.pailitao.com/search?q=&imgfile=1&js=1&stats_click=search_radio_all%253A1&initiative_id=staobaoz_20180702&ie=utf8&tfsid=TB17UrkjYZnBKNjSZFKXXcGOVXa&app=imgsearch')
# filter("shirt")
# r = requests.get(
#     'http://www.pailitao.com/search?q=http%3A%2F%2Fimg.alicdn.com%2Ftps%2Fi4%2FTB1INDTIpXXXXX5XVXXq4cC1VXX-642-642.jpg&imgfile=')
# print(r.headers)
# pic = request.urlopen('TB28j2Jc7CWBuNjy0FaXXXUlXXa_!!1670163060.jpg').read()
# f = open('f.jpg','wb')
# f.write(pic)
# scrapy('t/tt', 'http://fs.xicidaili.com/images/side.png')
