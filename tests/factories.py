import factory
from uuid import uuid4

from requests_queue.models import Request, StatusEvent


class RequestFactory(factory.Factory):
    class Meta:
        model = Request

    id = factory.Sequence(lambda x: uuid4())
