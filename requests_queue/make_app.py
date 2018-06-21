import os
import tornado.web
from tornado.web import url
from configparser import ConfigParser

from requests_queue.redis import make_redis
from requests_queue.database import make_db
from requests_queue.handlers.requests import RequestsHandler
from requests_queue.handlers.user_requests import UserRequestsHandler
from requests_queue.handlers.main import MainHandler


def make_app(config, deps):
    db_session = deps['db']

    app = tornado.web.Application([
            url( r'/', MainHandler),

            url(r'/v1/requests', RequestsHandler, {'db_session': db_session}),
            url(r'/v1/requests/(.*)', RequestsHandler, {'db_session': db_session}),

            url(r'/v1/users/(.*)/requests', UserRequestsHandler, {'db_session': db_session}),
            url(r'/v1/users/(.*)/requests/(.*)', UserRequestsHandler, {'db_session': db_session}),
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

def make_deps(config):
    return {
        'db': make_db(config)
    }
