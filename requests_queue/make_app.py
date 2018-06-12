import os
import tornado.web
from tornado.web import url
from configparser import ConfigParser

from requests_queue.redis import make_redis
from requests_queue.database import make_db
from requests_queue.handlers.request import RequestHandler
from requests_queue.handlers.main import MainHandler


def make_app(config):
    db_session = make_db(config)

    app = tornado.web.Application([
            url( r'/', MainHandler),
            url(r'/requests', RequestHandler, {'db_session': db_session}),
            url(r'/requests/(.*)', RequestHandler, {'db_session': db_session}),
        ],
        debug=config['default'].getboolean('DEBUG'),
    )
    return app


def make_config():
    BASE_CONFIG_FILENAME = os.path.join(
        os.path.dirname(__file__),
        '../config/base.ini',
    )
    ENV_CONFIG_FILENAME = os.path.join(
        os.path.dirname(__file__),
        '../config/',
        '{}.ini'.format(os.getenv('FLASK_ENV', 'dev').lower())
    )
    config = ConfigParser()

    # ENV_CONFIG will override values in BASE_CONFIG.
    config.read([BASE_CONFIG_FILENAME, ENV_CONFIG_FILENAME])
    return config
