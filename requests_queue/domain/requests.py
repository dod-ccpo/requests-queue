from requests_queue.models import Request

class Requests(object):

    def __init__(self, db_session):
        self.db_session = db_session

    def get(self, request_id):
        return self.db_session.query(Request).get(request_id)

    def get_many(self, creator_id=None):
        filters = []
        if creator_id:
            filters.append(Request.creator == creator_id)

        requests = (self.db_session.query(Request)
                                   .filter(*filters)
                                   .order_by(Request.time_created.desc())
                                   .all())
        return requests
