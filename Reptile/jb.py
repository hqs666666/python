import pika
import logging
import moment
import requests
import json
import time
import redis
import pa

class ReceiveData:
    mid = ''
    sendTime = ''
    title = ''
    content = ''
    request_url = ''
    red_url = ''


def getJbCode(body):
    params = getParams(body)
    code = requests.get(params.request_url)
    saveInRedis("jbcode", code.text)
    notification(params)

def getReptile(body):
    params = getParams(body)
    if(listExistValue("receive_msg",params.mid)):
        return
    res = pa.ImageDownload(params.request_url)
    params.red_url='http://reptile.t.cn/Home/Privacy?code='+res.imgKey
    dicts=res.convert_to_json(params)
    saveInRedis("receive_msg", dicts)
    logging.info('images download finish')  
    notification(params)

def getParams(body):
    body = str(body, encoding="utf-8")
    jsonObject = json.loads(body)
    data = ReceiveData()
    data.mid = jsonObject['Id']
    data.sendTime = jsonObject['SendTime']
    data.title = jsonObject['Title']
    data.content = jsonObject['Content']
    data.request_url = jsonObject['RequestUrl']
    data.red_url = jsonObject['ViewUrl']
    return data

def listExistValue(key,value):
    datalist = r.lrange(key,0,-1)
    values = list(filter(lambda x:json.loads(x)["Id"] == value),datalist)
    print(key,'中已存在',value,'跳过...')
    return not values

def saveInRedis(key, value):
    if (r.exists(key) == 1):
        r.lpushx(key, value)
    else:
        r.lpush(key, value)


def notification(message):
    url = 'http://hqs.pub:8080/ShR55Gn5TWJGp2d7AD6tFY/' + \
        message.title+'/'+message.content+'?url='+message.red_url
    requests.get(url)
    logging.info('request completed.mid='+message.mid)


def jbcode_callback(ch, method, properties, body):
    '''回调函数,处理从rabbitmq中取出的消息'''
    time.sleep(3)  # 等候3s 再往下执行
    logging.info('messgae received jbcode')
    getJbCode(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 执行完再ack消息
    logging.info('jbcode messgae is ack on'+str(moment.now()))


def reptile_callback(ch, method, properties, body):
    time.sleep(3)
    logging.info('messgae received reptile')
    getReptile(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 执行完再ack消息
    logging.info('reptile messgae is ack on'+str(moment.now()))


logging.getLogger().setLevel(logging.INFO)
logging.info('starting...')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='t.cn', port=5672, credentials=credentials))
logging.info('rebbitmq connecting')

channel = connection.channel()
channel.queue_declare(queue='queue_jbcode')
channel.queue_declare(queue='queue_reptile')

pool = redis.ConnectionPool(host='t.cn', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
logging.info('redis connecting')


channel.basic_qos(prefetch_count=1)  # 只有工作者完成任务之后，才会再次接收到任务
channel.basic_consume(jbcode_callback, queue='queue_jbcode', no_ack=False)
channel.basic_consume(reptile_callback, queue='queue_reptile', no_ack=False)
logging.info(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()  # 开始监听 接受消息
