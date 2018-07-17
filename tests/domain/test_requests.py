import pytest
from uuid import uuid4

from requests_queue.domain.requests import Requests
from requests_queue.domain.exceptions import NotFoundError

from tests.factories import RequestFactory

def test_can_get_request(requests: Requests, db):
    created_request = RequestFactory.create()
    db.add(created_request)
    db.commit()

    request = requests.get(created_request.id)

    assert request.id == created_request.id

def test_nonexistent_request_raises(requests: Requests):
    with pytest.raises(NotFoundError):
        requests.get(uuid4())
