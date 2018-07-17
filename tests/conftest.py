import pytest
from sqlalchemy.orm import sessionmaker, scoped_session

from requests_queue.make_app import make_app, make_deps, make_config
from requests_queue.database import make_db
from requests_queue.domain.requests import Requests

@pytest.fixture(scope='function')
def app(db):
    config = make_config()
    base_deps = make_deps(config)
    deps = {**base_deps, 'db': db}
    app = make_app(config, deps)
    return app


@pytest.fixture(scope='function')
def db():

    # Override db with a new SQLAlchemy session so that we can rollback
    # each test's transaction.
    # Inspiration: https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#session-external-transaction
    config = make_config()
    database = make_db(config)
    connection = database.get_bind().connect()
    transaction = connection.begin()
    db = scoped_session(sessionmaker(bind=connection))

    yield db

    db.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def requests(db):
    return Requests(db)
