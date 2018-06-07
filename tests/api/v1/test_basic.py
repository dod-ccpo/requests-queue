import pytest
from json import dumps

USER_ID = 'abcd-efgh'


@pytest.mark.gen_test
def test_hello_world(http_client, base_url):
    response = yield http_client.fetch(base_url)
    assert response.code == 200


@pytest.mark.gen_test
def test_new_request(http_client, base_url):
    response = yield http_client.fetch(
        base_url + '/requests',
        method='POST',
        body=dumps({
            'creator': '',
            'type': '',
            'body': {
            }
        }
    ))
