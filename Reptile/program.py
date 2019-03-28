import pika
import logging
import jetbrains_code
import weather
import capture_images


def consume(channel, queue, callback):
    channel.queue_declare(queue=queue)
    channel.basic_qos(prefetch_count=1)  # 只有工作者完成任务之后，才会再次接收到任务
    channel.basic_consume(callback, queue=queue, no_ack=False)


logging.getLogger().setLevel(logging.INFO)
logging.info('starting...')
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='t.cn', port=5672, credentials=credentials))
logging.info('rebbitmq connecting')


channel = connection.channel()
logging.info('receive....')
consume(channel, 'queue_jbcode', jetbrains_code.jetbrains_code().message_callback)
consume(channel, 'queue_reptile', capture_images.capture_images().message_callback)
consume(channel, 'queue_weather', weather.weather().message_callback)

channel.start_consuming()  # 开始监听 接收消息
