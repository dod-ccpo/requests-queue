import os
import tornado.web
from tornado.web import url
from configparser import ConfigParser

from requests_queue.database import make_db
from requests_queue.handlers.root import RootHandler
from requests_queue.handlers.status import StatusHandler
from requests_queue.handlers.requests import RequestsHandler
from requests_queue.handlers.requests_submit import RequestsSubmitHandler
from requests_queue.handlers.requests_index import RequestsIndexHandler


def make_app(config, deps):
    db_session = deps['db']
    prefix = '/api/v1'

    app = tornado.web.Application([
            url(r'/', RootHandler),
            url(r'/status', StatusHandler),

            url(prefix + r'/requests', RequestsIndexHandler, {'db_session': db_session}),
            url(prefix + r'/requests/(.*)/submit', RequestsSubmitHandler, {'db_session': db_session}),
            url(prefix + r'/requests/(.*)', RequestsHandler, {'db_session': db_session}),
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
