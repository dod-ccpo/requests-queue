from requests_queue.handlers.base import BaseHandler

from requests_queue.models import Request
from requests_queue.serializers.request import RequestSerializer


class UserRequestsHandler(BaseHandler):

    def initialize(self, db_session):
        self.db_session = db_session

    def get(self, user_id, request_id=None):
        if request_id:
            request = self.db_session.query(Request).get(request_id)
            if request is not None:
                serialized_request = RequestSerializer().dump(request).data
                self.write(serialized_request)
            else:
                self.send_error(404)
        else:
            requests = (self.db_session.query(Request)
                                       .filter(Request.creator == user_id)
                                       .all())
            serialized_requests = RequestSerializer().dump(requests, many=True).data
            self.write({'requests': serialized_requests})
