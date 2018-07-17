import tornado.gen
from tornado.ioloop import IOLoop

from requests_queue.handlers.base import BaseHandler
from requests_queue.serializers.request import RequestSerializer
from requests_queue.domain.requests import Requests
from requests_queue.domain.exceptions import NotFoundError
from .utils import parse_body


class RequestsHandler(BaseHandler):
    def initialize(self, db_session):
        self.db_session = db_session
        self.requests_repo = Requests(self.db_session)

    def patch(self, request_id):
        """
        Given a request_id and a request body, recursively merge the
        request body into the existing request's body.
        """

        json = parse_body(self.request)
        if not self.requests_repo.exists(request_id, json["creator_id"]):
            return self.send_error(404)

        IOLoop.current().spawn_callback(
            self.requests_repo.update, request_id, json["request"]
        )

        self.set_status(202)

    def get(self, request_id):
        try:
            request = self.requests_repo.get(request_id)
        except NotFoundError:
            self.send_error(404)

        serialized_request = RequestSerializer().dump(request).data
        self.write(serialized_request)
