import logging
import requests
import moment
import redis_helper
import utils
import time
import json
import pa

class capture_images(utils.utils):
    def message_callback(self,ch, method, properties, body):
        logging.info('messgae received reptile')
        time.sleep(1)
        self.__get_reptile(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 执行完再ack消息
        logging.info('jbcode messgae is ack on :'+str(moment.now()))

    def __get_reptile(self,body):
        params = self.get_params(body)
        redis = redis_helper.redis_helper()
        datalist =redis.get_value('receive_msg')
        values = list(filter(lambda x:json.loads(x)["Id"] == params.mid),datalist)

        if not values:
            logging.info('receive_msg中已存在'+params.mid+'跳过...')
            return

        res = pa.ImageDownload(params.request_url)
        params.red_url='http://reptile.t.cn/Home/Privacy?code='+res.imgKey
        dicts=res.convert_to_json(params)
        redis.set_value("receive_msg", dicts)
        logging.info('images download finish')  
        self.notification(params)