from json import loads
from tornado.web import RequestHandler

from requests_queue.models import Request
from requests_queue.serializers.request import RequestSerializer


def parse_body(request):
    return loads(request.body.decode('utf-8'))

class RequestHandler(RequestHandler):

    def initialize(self, db_session):
        self.db_session = db_session

    def get(self, request_id):
        return self.write({})

    def post(self):
        json = parse_body(self.request)
        request = Request(creator=json['creator_id'], body=json['request'])
        self.db_session.add(request)
        self.db_session.commit()
        self.write(RequestSerializer().dump(request).data)
