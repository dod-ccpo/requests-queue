from sqlalchemy import create_engine


def make_db(config):
    engine = create_engine(config['default']['DATABASE_URI'])
    return engine
