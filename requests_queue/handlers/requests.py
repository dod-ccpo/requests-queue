from json import loads
import tornado.gen
from tornado.ioloop import IOLoop

from requests_queue.handlers.base import BaseHandler
from requests_queue.models import Request, StatusEvent
from requests_queue.serializers.request import RequestSerializer
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.attributes import flag_modified


def should_allow_submission(request):
    all_request_sections = ["details_of_use", "information_about_you", "primary_poc"]
    existing_request_sections = request.body.keys()
    return request.status == "incomplete" and all(
        section in existing_request_sections for section in all_request_sections
    )


@tornado.gen.coroutine
def update_request(db_session, request, request_delta):
    request.body = deep_merge(request_delta, request.body)

    if should_allow_submission(request):
        request.status_events.append(StatusEvent(new_status="pending_submission"))

    # Without this, sqlalchemy won't notice the change to request.body,
    # since it doesn't track dictionary mutations by default.
    flag_modified(request, "body")

    db_session.add(request)
    db_session.commit()

    return None


def parse_body(request):
    return loads(request.body.decode("utf-8"))


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


class RequestsHandler(BaseHandler):
    def initialize(self, db_session):
        self.db_session = db_session

    def patch(self, request_id):
        """
        Given a request_id and a request body, recursively merge the
        request body into the existing request's body.
        """
        json = parse_body(self.request)
        try:
            # Query for request matching id, acquiring a row-level write lock.
            # https://www.postgresql.org/docs/10/static/sql-select.html#SQL-FOR-UPDATE-SHARE
            request = (
                self.db_session.query(Request)
                .filter_by(id=request_id, creator=json["creator_id"])
                .with_for_update(of=Request)
                .one()
            )
        except NoResultFound:
            return self.send_error(404)

        IOLoop.current().spawn_callback(
            update_request, self.db_session, request, json["request"]
        )

        self.set_status(202)

    def post(self):
        json = parse_body(self.request)

        request = Request(creator=json["creator_id"], body=json["request"])
        status_event = StatusEvent(new_status="incomplete")
        request.status_events.append(status_event)
        self.db_session.add(request)
        self.db_session.commit()

        self.set_status(202)
        self.write(RequestSerializer().dump(request).data)
