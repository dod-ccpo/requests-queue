from requests_queue.make_app import make_config
from requests_queue.database import make_db
from requests_queue.models import *

db = make_db(make_config())

print("\nWelcome to requests-queue. This shell has all models in scope, and a SQLAlchemy session called db.")
