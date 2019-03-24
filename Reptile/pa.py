import re
import random
from pyquery import PyQuery as pq
import requests
import moment
import os
import urllib.parse
import uuid
import json
import redis


class ImageDownload:
    def __getImgList(self, url):
        res = requests.get(url)
        text = res.text
        html = pq(text)
        imgs = html('img')
        return imgs

    def __downloadImg(self, imgList, folder):
        x = 1
        for imgurl in imgList:
            try:
                url = self.__getImgSrc(imgurl)
                if(not url):
                    continue
                print(url)
                img = requests.get(url, timeout=5)
                if(img.status_code != 200):
                    print('第', x, '张图片下载失败url=', url)
                    continue

                fileType = self.__getFileType(url)
                fileName = self.__getFileName()
                imgfile = folder+fileName+'.'+fileType
                fo = open(imgfile, 'wb')
                fo.write(img.content)
                fo.close()
                self.__save(imgfile)
                print('第', x, '张图片下载完成', url, '文件名', fileName)
                x += 1
            except requests.exceptions.RequestException as e:
                print(e)
                continue

    def __getFileType(self, fileName):
        array = fileName.split('.')
        return array[-1]

    def __getFileName(self):
        filename = uuid.uuid1()
        return str(filename)

    def __getImgSrc(self, html):
        img = self.__getHtmlAttr(html, 'src')
        if(not img):
            return img
        if('static' in img):
            img = self.__getHtmlAttr(html, 'data-original')
        return img

    def __getHtmlAttr(self, html, attr):
        p = pq(html)
        d = p.attr(attr)
        return d

    def __extractDomainFromURL(self, url):
        parsed_uri = urllib.parse.urlparse(url)
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        return domain

    def __load(self, url):
        imgs = self.__getImgList(url)
        if not imgs:
            return

        date = moment.now().format("YYYY-M-D")
        domain = self.__extractDomainFromURL(url)
        ran = str(random.randint(100, 100000))
        folder = '/reptile/pics/'+date+'/'+domain+'/'+ran+'/'
        self.imgKey = domain+str(uuid.uuid1())
        print(folder)

        if not os.path.exists(folder):
            os.makedirs(folder)
        self.__downloadImg(imgs, folder)

    def __save(self, value):
        if (self.r.exists(self.imgKey) == 1):
            self.r.lpushx(self.imgKey, value)
        else:
            self.r.lpush(self.imgKey, value)

    def __init__(self, url):
        self.__load(url)

    def convert_to_json(self, obj):
        '''把Object对象转换成Dict对象'''
        dict = {}
        dict.update(obj.__dict__)
        jj = json.dumps(dict)
        return jj

    pool = redis.ConnectionPool(host='t.cn', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    imgKey=''
