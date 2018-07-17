from json import loads
import tornado.gen
from tornado.ioloop import IOLoop
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import exists, and_

from requests_queue.handlers.base import BaseHandler
from requests_queue.models import Request, StatusEvent
from requests_queue.serializers.request import RequestSerializer
from requests_queue.domain.requests import Requests
from .utils import parse_body


class RequestsIndexHandler(BaseHandler):
    def initialize(self, db_session):
        self.db_session = db_session
        self.requests_repo = Requests(self.db_session)

    def post(self):
        json = parse_body(self.request)
        request = self.requests_repo.create(json["creator_id"], json["request"])
        self.set_status(202)
        self.write(RequestSerializer().dump(request).data)

    def get(self, **kwargs):
        creator_id = self.get_argument('creator_id', None)
        requests = self.requests_repo.get_many(creator_id=creator_id)
        serialized_requests = RequestSerializer().dump(requests, many=True).data
        self.write({'requests': serialized_requests})
