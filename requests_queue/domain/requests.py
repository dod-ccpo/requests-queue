import tornado.gen
from sqlalchemy import exists, and_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.attributes import flag_modified

from requests_queue.models import Request, StatusEvent
from .exceptions import NotFoundError
from .utils import deep_merge


class Requests(object):
    def __init__(self, db_session):
        self.db_session = db_session

    def create(self, creator_id, body):
        request = Request(creator=creator_id, body=body)

        status_event = StatusEvent(new_status="incomplete")
        request.status_events.append(status_event)

        self.db_session.add(request)
        self.db_session.commit()

        return request

    def exists(self, request_id, creator_id):
        return self.db_session.query(
            exists().where(
                and_(Request.id == request_id, Request.creator == creator_id)
            )
        ).scalar()

    def get(self, request_id):
        try:
            request = self.db_session.query(Request).filter_by(id=request_id).one()
        except NoResultFound:
            raise NotFoundError("request")

        return request

    def get_many(self, creator_id=None):
        filters = []
        if creator_id:
            filters.append(Request.creator == creator_id)

        requests = (
            self.db_session.query(Request)
            .filter(*filters)
            .order_by(Request.time_created.desc())
            .all()
        )
        return requests

    @tornado.gen.coroutine
    def submit(self, request):
        request.status_events.append(StatusEvent(new_status="submitted"))

        if Requests.should_auto_approve(request):
            request.status_events.append(StatusEvent(new_status="approved"))

        self.db_session.add(request)
        self.db_session.commit()

        return request

    @tornado.gen.coroutine
    def update(self, request_id, request_delta):
        try:
            # Query for request matching id, acquiring a row-level write lock.
            # https://www.postgresql.org/docs/10/static/sql-select.html#SQL-FOR-UPDATE-SHARE
            request = (
                self.db_session.query(Request)
                .filter_by(id=request_id)
                .with_for_update(of=Request)
                .one()
            )
        except NoResultFound:
            return

        request.body = deep_merge(request_delta, request.body)

        if Requests.should_allow_submission(request):
            request.status_events.append(StatusEvent(new_status="pending_submission"))

        # Without this, sqlalchemy won't notice the change to request.body,
        # since it doesn't track dictionary mutations by default.
        flag_modified(request, "body")

        db_session.add(request)
        db_session.commit()

    @classmethod
    def should_auto_approve(cls, request):
        all_request_sections = [
            "details_of_use",
            "information_about_you",
            "primary_poc",
        ]
        existing_request_sections = request.body.keys()
        return request.status == "submitted" and all(
            section in existing_request_sections for section in all_request_sections
        )

    @classmethod
    def should_allow_submission(cls, request):
        all_request_sections = [
            "details_of_use",
            "information_about_you",
            "primary_poc",
        ]
        existing_request_sections = request.body.keys()
        return request.status == "incomplete" and all(
            section in existing_request_sections for section in all_request_sections
        )
