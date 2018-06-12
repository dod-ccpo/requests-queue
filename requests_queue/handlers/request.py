from json import loads
from tornado.web import RequestHandler


def parse_body(request):
    return loads(request.body.decode('utf-8'))

class RequestHandler(RequestHandler):

    def initialize(self, redis):
        self.redis = redis

    def get(self, request_id):
        return self.write({})

    def post(self):
        body = parse_body(self.request)

