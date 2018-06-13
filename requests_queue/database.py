from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def make_db(config):
    engine = create_engine(config['default']['DATABASE_URI'])
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()
