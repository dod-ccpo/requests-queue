import tornado.gen
from sqlalchemy.orm.exc import NoResultFound

from requests_queue.models import Request, StatusEvent
from .exceptions import NotFoundError

class Requests(object):

    def __init__(self, db_session):
        self.db_session = db_session

    def get(self, request_id):
        try:
            request = (
                self.db_session.query(Request)
                .filter_by(id=request_id)
                .one()
            )
        except NoResultFound:
            raise NotFoundError("request")

        return request

    def get_many(self, creator_id=None):
        filters = []
        if creator_id:
            filters.append(Request.creator == creator_id)

        requests = (self.db_session.query(Request)
                                   .filter(*filters)
                                   .order_by(Request.time_created.desc())
                                   .all())
        return requests

    @tornado.gen.coroutine
    def submit(self, request):
        request.status_events.append(StatusEvent(new_status="submitted"))

        if Requests.should_auto_approve(request):
            request.status_events.append(StatusEvent(new_status="approved"))

        self.db_session.add(request)
        self.db_session.commit()

    @classmethod
    def should_auto_approve(cls, request):
        all_request_sections = ["details_of_use", "information_about_you", "primary_poc"]
        existing_request_sections = request.body.keys()
        return request.status == "submitted" and all(
            section in existing_request_sections for section in all_request_sections
        )
