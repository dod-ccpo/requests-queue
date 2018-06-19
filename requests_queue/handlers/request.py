from json import loads
from tornado.web import RequestHandler

from requests_queue.models import Request
from requests_queue.serializers.request import RequestSerializer
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.attributes import flag_modified


def parse_body(request):
    return loads(request.body.decode('utf-8'))


def deep_merge(source, destination: dict):
    """
    Merge source dict into destination dict recursively.
    """
    def _deep_merge(a, b):
        for key, value in a.items():
            if isinstance(value, dict):
                node = b.setdefault(key, {})
                _deep_merge(value, node)
            else:
                b[key] = value

        return b
    return _deep_merge(source, dict(destination))


class RequestHandler(RequestHandler):

    def initialize(self, db_session):
        self.db_session = db_session

    def get(self, request_id=None):
        if request_id:
            request = self.db_session.query(Request).get(request_id)
            if request is not None:
                serialized_request = RequestSerializer().dump(request).data
                self.write(serialized_request)
            else:
                self.send_error(404)
        else:
            creator_id = self.get_argument('creator_id', None)
            requests = (self.db_session.query(Request)
                                       .filter(Request.creator == creator_id)
                                       .all())
            serialized_requests = RequestSerializer().dump(requests, many=True).data
            self.write({'requests': serialized_requests})

    def patch(self, request_id):
        """
        Given a request_id and a request body, recursively merge the
        request body into the existing request's body.
        """
        json = parse_body(self.request)
        try:
            # Query for request matching id, acquiring a row-level write lock.
            # https://www.postgresql.org/docs/10/static/sql-select.html#SQL-FOR-UPDATE-SHARE
            request = self.db_session.query(Request) \
                                     .filter(Request.id == request_id) \
                                     .with_for_update(of=Request) \
                                     .one()
        except NoResultFound:
            return self.send_error(404)

        request.body = deep_merge(json, request.body)

        # Without this, sqlalchemy won't notice the change to request.body,
        # since it doesn't track dictionary mutations by default.
        flag_modified(request, 'body')

        self.db_session.commit()

        self.set_status(202)


    def post(self):
        json = parse_body(self.request)
        request = Request(creator=json['creator_id'], body=json['request'])
        self.db_session.add(request)
        self.db_session.commit()

        self.set_status(202)
        self.write(RequestSerializer().dump(request).data)
