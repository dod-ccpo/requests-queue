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
def test_auto_approve_less_than_1m(requests, db):
    created_request = RequestFactory.create()
    db.add(created_request)
    db.commit()

    created_request.body = {"details_of_use": {"dollar_value": 999999}}

    request = yield requests.submit(created_request)

    assert request.status == 'approved'


@pytest.mark.gen_test
def test_dont_auto_approve_if_dollar_value_is_1m_or_above(requests, db):
    created_request = RequestFactory.create()
    db.add(created_request)
    db.commit()

    created_request.body = {"details_of_use": {"dollar_value": 1000000}}

    request = yield requests.submit(created_request)

    assert request.status == 'submitted'


@pytest.mark.gen_test
def test_dont_auto_approve_if_no_dollar_value_specified(requests, db):
    created_request = RequestFactory.create()
    db.add(created_request)
    db.commit()

    created_request.body = {"details_of_use": {}}

    request = yield requests.submit(created_request)

    assert request.status == 'submitted'
