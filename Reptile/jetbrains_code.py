import logging
import requests
import moment
import redis_helper
import utils
import time

class jetbrains_code(utils.utils):
    def message_callback(self,ch, method, properties, body):
        logging.info('messgae received jbcode')
        time.sleep(1)
        self.__get_jbcode(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 执行完再ack消息
        logging.info('jbcode messgae is ack on :'+str(moment.now()))

    def __get_jbcode(self,body):
        params = self.get_params(body)
        code = requests.get(params.request_url)
        redis = redis_helper.redis_helper()
        redis.set_value("jbcode", code.text)
        self.notification(params)

    