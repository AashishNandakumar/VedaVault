from urllib.parse import urlparse

import redis
from django.conf import settings

redis_url = urlparse(settings.CACHES['default']['LOCATION'])
redis_host = redis_url.hostname
redis_port = redis_url.port

redis_instance = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)


class RedisCache:
    @staticmethod
    def set_instance(**kwargs):
        username = kwargs['username']
        otp = kwargs['otp']

        redis_instance.set(username, otp, ex=500)  # change the 'ex' in production

    @staticmethod
    def get_instance(**kwargs):
        username = kwargs['username']

        return redis_instance.get(username)
