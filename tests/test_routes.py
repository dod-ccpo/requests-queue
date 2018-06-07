import pytest


@pytest.mark.gen_test
def test_routes(http_client, base_url):
    for path in (
            '/',
            '/requests/1'
            ):
        response = yield http_client.fetch(base_url + path)
    assert response.code == 200
