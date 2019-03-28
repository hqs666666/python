import redis
import logging
import json


class redis_helper:
    def __init__(self):
        pool = redis.ConnectionPool(
            host='t.cn', port=6379, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)
        logging.info('redis connecting')

    def set_value(self, key, value):
        if (self.r.exists(key) == 1):
            self. r.lpushx(key, value)
        else:
            self.r.lpush(key, value)
        logging.info('redis set key successfully')

    def get_value(self, key):
        if (self.r.exists(key) == 1):
            logging.info('redis get key successfully')
            value = self.r.lrange(key, 0, -1)
            return value
        else:
            logging.info('the key not exist')
            return
