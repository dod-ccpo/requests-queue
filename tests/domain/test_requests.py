import pytest
from uuid import uuid4

from requests_queue.domain.exceptions import NotFoundError

from tests.factories import RequestFactory


def test_can_get_request(requests, db):
    created_request = RequestFactory.create()
    db.add(created_request)
    db.commit()

    request = requests.get(created_request.id)

    assert request.id == created_request.id


def test_nonexistent_request_raises(requests):
    with pytest.raises(NotFoundError):
        requests.get(uuid4())


@pytest.mark.gen_test
def test_auto_approve_200k_or_less(requests, db):
    created_request = RequestFactory.create()
    db.add(created_request)
    db.commit()

    created_request.body = {"details_of_use": {"dollar_value": 200000}}

    request = yield requests.submit(created_request)

    assert request.status == 'approved'
