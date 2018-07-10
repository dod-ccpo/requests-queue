from requests_queue.make_app import make_config
from requests_queue.database import make_db
from requests_queue.models import *

db = make_db(make_config())
