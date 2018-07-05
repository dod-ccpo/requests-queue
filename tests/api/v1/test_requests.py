import pytest
from json import dumps, loads

sample_request_body = {
    "details_of_use": {
        "pe_id": "123",
        "uii_ids": "1\r\n2\r\n3",
        "total_ram": 2,
        "date_start": "2018-07-02",
        "total_cores": 1,
        "dollar_value": 100,
        "app_description": "Hello",
        "num_applications": 1,
        "has_migration_office": "yes",
        "total_object_storage": 3,
        "total_server_storage": 5,
        "has_contractor_advisor": "yes",
        "total_database_storage": 4,
        "supported_organizations": "army",
        "supporting_organization": "AF CCE/HNI",
        "is_migrating_application": "yes",
    },
    "information_about_you": {
        "citizenship": "United States",
        "designation": "hello",
        "phone_number": "7728349265",
        "email_request": "meow@hello.com",
        "fname_request": "Richard",
        "lname_request": "Howard",
        "service_branch": "army",
        "date_latest_training": "2018-06-24",
    },
    "primary_poc": {
        "dodid_poc": "1234567890",
        "email_poc": "richard@promptworks.com",
        "fname_poc": "a",
        "lname_poc": "b",
    },
}

sample_post_body = {
    'creator_id': 'e59a9d20-c31e-47f5-a9ae-d791ad8fffa4',
    'request': sample_request_body,
}


@pytest.mark.gen_test
def test_create_request(http_client, base_url):
    response = yield http_client.fetch(
        base_url + '/api/v1/requests',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=dumps(sample_post_body))
    assert response.code == 202
    assert 'id' in loads(response.body)


@pytest.mark.gen_test
def test_update_request(http_client, base_url):
    creator_id = 'bf53276a-29e0-476c-b820-b313ec19ec7f'
    sample_request = {
        'creator_id': creator_id,
        'request': {
            'red': {
                'a': 1,
                'b': 2,
                'c': 3
            },
            'green': [1, 2, 3],
            'blue': 3
        }
    }
    response = yield http_client.fetch(
        base_url + '/api/v1/requests',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=dumps(sample_request))
    request_id = loads(response.body)['id']

    request_delta = {
        'creator_id': creator_id,
        'request': {
            'red': {'b': 20}
        }
    }

    response = yield http_client.fetch(
        base_url + '/api/v1/requests/{}'.format(request_id),
        method='PATCH',
        headers={'Content-Type': 'application/json'},
        body=dumps(request_delta)
    )
    assert response.code == 202

@pytest.mark.gen_test
def test_update_nonexistent_request(http_client, base_url):
    response = yield http_client.fetch(
        base_url + '/api/v1/requests/{}'.format('bf53276a-29e0-476c-b820-b313ec19ec7d'),
        method='PATCH',
        headers={'Content-Type': 'application/json'},
        body=dumps({
            'creator_id': '4fa5efcf-8772-473f-8767-3c6c23b41bf3',
            'a': 'b'
        }),
        raise_error=False)
    assert response.code == 404


@pytest.mark.gen_test
def test_get_user_requests(http_client, base_url):
    user_id = '5c40a181-c669-4d9f-8273-3564bc3f41ff'
    response = yield http_client.fetch(
        base_url + '/api/v1/users/{}/requests'.format(user_id),
        method='GET',
        headers={'Content-Type': 'application/json'})
    assert response.code == 200
    response_json = loads(response.body)
    assert 'requests' in response_json


@pytest.mark.gen_test
def test_get_user_request(http_client, base_url):
    response = yield http_client.fetch(
        base_url + '/api/v1/requests',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=dumps(sample_post_body))
    request_id = loads(response.body)['id']

    response = yield http_client.fetch(
        '{}/api/v1/users/{}/requests/{}'.format(
            base_url, sample_post_body['creator_id'], request_id),
        method='GET')
    assert response.code == 200
    assert loads(response.body)['id'] == request_id

@pytest.mark.gen_test
def test_request_starts_out_pending(http_client, base_url):
    response = yield http_client.fetch(
        base_url + '/api/v1/requests',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=dumps(sample_post_body))
    request_id = loads(response.body)['id']

    response = yield http_client.fetch(
        '{}/api/v1/users/{}/requests/{}'.format(
            base_url, sample_post_body['creator_id'], request_id),
        method='GET')
    assert response.code == 200
    assert loads(response.body)['status'] == 'pending'


@pytest.mark.gen_test
def test_submit_triggers_auto_approval(http_client, base_url):
    response = yield http_client.fetch(
        base_url + '/api/v1/requests',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=dumps(sample_post_body))
    request_id = loads(response.body)['id']

    yield http_client.fetch(
        base_url + '/api/v1/requests/{}/submit'.format(request_id),
        method='POST',
        body=dumps({}),
        headers={'Content-Type': 'application/json'}
    )

    response = yield http_client.fetch(
        '{}/api/v1/users/{}/requests/{}'.format(
            base_url, sample_post_body['creator_id'], request_id),
        method='GET')
    assert response.code == 200
    assert loads(response.body)['status'] == 'approved'
