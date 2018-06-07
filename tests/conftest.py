import pytest
from requests_queue.make_app import make_app, make_config


@pytest.fixture(scope='session')
def app():
    return make_app(make_config())
