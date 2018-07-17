import pytest
from requests_queue.make_app import make_app, make_deps, make_config
from sqlalchemy.orm import sessionmaker, scoped_session


@pytest.fixture(scope='function')
def app():
    config = make_config()
    base_deps = make_deps(config)

    # Override db with a new SQLAlchemy session so that we can rollback
    # each test's transaction.
    # Inspiration: https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#session-external-transaction
    connection = base_deps['db'].get_bind().connect()
    transaction = connection.begin()
    db = scoped_session(sessionmaker(bind=connection))
    deps = {**base_deps, 'db': db}

    app = make_app(config, deps)

    yield app

    db.close()
    transaction.rollback()
    connection.close()
