import pytest
from json import loads


@pytest.mark.gen_test
def test_status_route(http_client, base_url):
    response = yield http_client.fetch(base_url + '/status')
    assert response.code == 200
    assert loads(response.body) == {'status': 'ok'}
