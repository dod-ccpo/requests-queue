import pytest


@pytest.mark.gen_test
def test_root_route(http_client, base_url):
    response = yield http_client.fetch(base_url)
    assert response.code == 200
    assert response.body == b'Hello from requests-queue'
