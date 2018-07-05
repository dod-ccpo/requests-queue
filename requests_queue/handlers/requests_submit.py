import tornado.gen
from tornado.ioloop import IOLoop

from requests_queue.handlers.base import BaseHandler
from requests_queue.models import Request, StatusEvent
from sqlalchemy.orm.exc import NoResultFound


def should_auto_approve(request):
    all_request_sections = ["details_of_use", "information_about_you", "primary_poc"]
    existing_request_sections = request.body.keys()
    return request.status == "submitted" and all(
        section in existing_request_sections for section in all_request_sections
    )


@tornado.gen.coroutine
def submit_request(db_session, request):
    request.status_events.append(StatusEvent(new_status="submitted"))

    if should_auto_approve(request):
        request.status_events.append(StatusEvent(new_status="approved"))

    db_session.add(request)
    db_session.commit()


class RequestsSubmitHandler(BaseHandler):
    def initialize(self, db_session):
        self.db_session = db_session

    def post(self, request_id):
        """
        Submit a request.
        """
        try:
            request = (
                self.db_session.query(Request)
                .filter_by(id=request_id)
                .with_for_update(of=Request)
                .one()
            )
        except NoResultFound:
            return self.send_error(404)

        IOLoop.current().spawn_callback(
            submit_request, self.db_session, request
        )

        self.set_status(202)
