import pytest
from json import dumps, loads
import pendulum


sample_request_body = {
    'details_of_use': {
        'application_details': {
            'application_name': 'Death Star VM',
            'application_description': 'A moon-sized space station with abilities to destroy stuff.',
            'estimated_use_dollars': 100000000,
            'estimation_method': 'csp_usage_calculator',
            'expected_start_date': pendulum.datetime(2018, 10, 1, 0, 0, 0).isoformat(),
            'expected_usage_months': 6,
            'classification_level': 'unclassified',
            'service_branch': ['air_force', 'marines']
        },
        'computation': {
            'num_vcpu_cores': 200,
            'total_ram': 30000000000000,
        },
        'storage': {
            'object_storage': 4000000000,
            'server_storage': 8000000000
        },
        'estimated_application_usage': {
            'active_users': 240000,
            'peak_concurrent_users': 100000,
            'requests_per_min_user': 100000000,
            'environments': 4,
        },
    },
    'professional_services': {
        'have_migration_contractor': True,
        'have_cloud_contractor': True,
        'need_cloud_contractor': False,
        'will_be_developed_by_contractor': True,
        'needs_native_cloud_infrastructure': True,
    },
    'organization': {
        'user': {
            'name': 'Friedrich Straat',
            'email': 'fstraat@dds.mil',
            'phone': '1234567890',
            'location': 'Ft. Gordon',
            'organization': 'DDS',
            'office_symbol': 'Department of Defense',
            'citizenship': 'foreign_national',
            'designation': 'military',
            'latest_ia_completion_date': '',
            'collaborators': [
                {
                    'name': 'Pietro Quirinis',
                    'email': 'quirinis@gov.mil',
                    'role': 'contracting_officer'
                },
                {
                    'name': '',
                    'email': '',
                    'role': 'financial_manager'
                }
            ]
        }
    },
    'task_order': {
        'order_number': '1234',
        'funding_type': 'rdte'
    }
}

sample_post_body = {
    'creator_id': 'e59a9d20-c31e-47f5-a9ae-d791ad8fffa4',
    'request': sample_request_body,
}


@pytest.mark.gen_test
def test_create_request(http_client, base_url):
    response = yield http_client.fetch(
        base_url + '/requests',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=dumps(sample_post_body))
    assert response.code == 202
    assert 'id' in loads(response.body)


@pytest.mark.gen_test
def test_update_request(http_client, base_url):
    sample_request = {
        'creator_id': 'bf53276a-29e0-476c-b820-b313ec19ec7f',
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
        base_url + '/requests',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=dumps(sample_request))
    request_id = loads(response.body)['id']

    request_delta = {
        'red': {'b': 20}
    }

    response = yield http_client.fetch(
        base_url + '/requests/{}'.format(request_id),
        method='PATCH',
        headers={'Content-Type': 'application/json'},
        body=dumps(request_delta)
    )
    assert response.code == 202

@pytest.mark.gen_test
def test_update_nonexistent_request(http_client, base_url):
    response = yield http_client.fetch(
        base_url + '/requests/{}'.format('bf53276a-29e0-476c-b820-b313ec19ec7d'),
        method='PATCH',
        headers={'Content-Type': 'application/json'},
        body=dumps({'a': 'b'}),
        raise_error=False)
    assert response.code == 404


@pytest.mark.gen_test
def test_get_requests(http_client, base_url):
    response = yield http_client.fetch(
        base_url + '/requests',
        method='GET',
        headers={'Content-Type': 'application/json'})
    assert response.code == 200
    response_json = loads(response.body)
    assert 'requests' in response_json
