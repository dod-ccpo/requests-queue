from redis import StrictRedis


def make_redis(config):
    return StrictRedis.from_url(
        config['default']['REDIS_URI'],
        decode_responses=True
    )
