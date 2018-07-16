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

partial_request_body = {
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
}

sample_post_body = {
    'creator_id': 'e59a9d20-c31e-47f5-a9ae-d791ad8fffa4',
    'request': sample_request_body,
}

partial_post_body = {
    'creator_id': 'e59a9d20-c31e-47f5-a9ae-d791ad8fffa4',
    'request': partial_request_body,
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

    response = yield http_client.fetch(
        base_url + '/api/v1/requests/{}'.format(request_id),
        method='GET',
        headers={'Content-Type': 'application/json'}
    )
    assert loads(response.body)['body'] == {
        'red': {
            'a': 1,
            'b': 20,
            'c': 3
        },
        'green': [1, 2, 3],
        'blue': 3
    }

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
        base_url + '/api/v1/requests?creator_id={}'.format(user_id),
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
        '{}/api/v1/requests/{}'.format(
            base_url, request_id),
        method='GET')
    assert response.code == 200
    assert loads(response.body)['id'] == request_id

@pytest.mark.gen_test
def test_get_all_requests(http_client, base_url):
    response = yield http_client.fetch(base_url + '/api/v1/requests', method='GET')
    pre_test_requests_count = len(loads(response.body)["requests"])

    response = yield http_client.fetch(
        base_url + '/api/v1/requests',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=dumps(sample_post_body))

    sample_post_body2 = dict(sample_post_body)
    sample_post_body2["creator_id"] = "1763e7ba-153b-41ff-b148-a7c23beea659"

    yield http_client.fetch(
        base_url + '/api/v1/requests',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=dumps(sample_post_body2))

    response = yield http_client.fetch(base_url + '/api/v1/requests', method='GET')
    assert response.code == 200

    requests = loads(response.body)["requests"]
    assert len(requests) == pre_test_requests_count + 2

@pytest.mark.gen_test
def test_get_requests_by_creator_id(http_client, base_url):
    response = yield http_client.fetch(
        base_url + '/api/v1/requests',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=dumps(sample_post_body))

    sample_post_body2 = dict(sample_post_body)
    sample_post_body2["creator_id"] = "1763e7ba-153b-41ff-b148-a7c23beea659"

    yield http_client.fetch(
        base_url + '/api/v1/requests',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=dumps(sample_post_body2))

    response = yield http_client.fetch(
        '{}/api/v1/requests?creator_id={}'.format(
            base_url, sample_post_body['creator_id']
        ),
        method='GET'
    )
    assert response.code == 200

    requests = loads(response.body)["requests"]
    assert len(requests) == 1

@pytest.mark.gen_test
def test_request_starts_out_incomplete(http_client, base_url):
    response = yield http_client.fetch(
        base_url + '/api/v1/requests',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=dumps(partial_post_body))
    request_id = loads(response.body)['id']

    response = yield http_client.fetch(
        '{}/api/v1/requests/{}'.format(
            base_url, request_id),
        method='GET')
    assert response.code == 200
    assert loads(response.body)['status'] == 'incomplete'

@pytest.mark.gen_test
def test_finishing_request_moves_it_to_pending_submission(http_client, base_url):
    creator_id = '9dcbb00f-e171-41c8-80e9-40ada34a4bc8'
    response = yield http_client.fetch(
        base_url + '/api/v1/requests',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=dumps({'creator_id': creator_id, 'request': {'incomplete': 'request'}}))
    request_id = loads(response.body)['id']


    response = yield http_client.fetch(
        base_url + '/api/v1/requests/{}'.format(request_id),
        method='PATCH',
        headers={'Content-Type': 'application/json'},
        body=dumps({'creator_id': creator_id, 'request': sample_request_body}))

    response = yield http_client.fetch(
        '{}/api/v1/requests/{}'.format(
            base_url, request_id),
        method='GET')
    assert loads(response.body)['status'] == 'pending_submission'


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
        '{}/api/v1/requests/{}'.format(
            base_url, request_id),
        method='GET')
    assert response.code == 200
    assert loads(response.body)['status'] == 'approved'
