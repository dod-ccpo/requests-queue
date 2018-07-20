from tornado.ioloop import IOLoop

from requests_queue.handlers.base import BaseHandler
from requests_queue.domain.requests import Requests
from requests_queue.domain.exceptions import NotFoundError


class RequestsSubmitHandler(BaseHandler):
    def initialize(self, db_session):
        self.db_session = db_session
        self.requests_repo = Requests(self.db_session)

    def post(self, request_id):
        """
        Submit a request.
        """

        try:
            request = self.requests_repo.get(request_id)
        except NotFoundError:
            return self.send_error(404)

        IOLoop.current().spawn_callback(
            self.requests_repo.submit, request
        )

        self.set_status(202)
