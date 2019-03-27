import logging
import requests
import json
import receive

class utils(object):
    def get_params(self,body):
        body = str(body, encoding="utf-8")
        jsonObject = json.loads(body)
        data = receive.receive_data()
        data.mid = jsonObject['Id']
        data.sendTime = jsonObject['SendTime']
        data.title = jsonObject['Title']
        data.content = jsonObject['Content']
        data.request_url = jsonObject['RequestUrl']
        data.red_url = jsonObject['ViewUrl']
        return data

    def notification(self,message):
        url = 'http://hqs.pub:8080/ShR55Gn5TWJGp2d7AD6tFY/' + \
        message.title+'/'+message.content+'?url='+message.red_url
        requests.get(url)
        logging.info('request completed.mid='+message.mid)