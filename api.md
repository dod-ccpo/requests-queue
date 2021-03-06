# Requests Queue API

## Requests

### Create request

Create a new JEDI request.

#### Request

```json
POST /api/v1/requests

{
    "creator_id": "164497f6-c1ea-4f42-a5ef-101da278c012",
    "request": {

    }
}

```

#### Response

A `202 Accepted` response with no body.

### Update request

Update an existing request.

#### Request

```json
PATCH /api/v1/requests/<request_id>

{
    "creator_id": "164497f6-c1ea-4f42-a5ef-101da278c012",
    "request": {

    }
}
```

#### Response

A `202 Accepted` response with no body.

### Submit request

Submit a request.

#### Request

```json
POST /api/v1/requests/<request_id>/submit
```

#### Response

A `202 Accepted` response with no body.

### Get requests

Get a list of a user's requests.

#### Request

```
GET /api/v1/users/<user_id>/requests?creator_id=164497f6-c1ea-4f42-a5ef-101da278c012
```

##### Arguments

- `creator_id`: Filters the list of requests to a given user id. If this param is not provided, all requests will be returned.

#### Response

```json
[
    {
        "body": {
            "primary_poc": {
                "dodid_poc": "1234567890",
                "email_poc": "richard@promptworks.com",
                "fname_poc": "r",
                "lname_poc": "Howard"
            }
        },
        "creator": "164497f6-c1ea-4f42-a5ef-101da278c012",
        "id": "8b3e61c7-d727-4983-962d-1f273d1ae2ee",
        "status": "incomplete",
        "time_created": "2018-07-09T17:12:20.708670+00:00"
    },
    ...
]
```

### Get request

Retrieve a request.

Request:

```
GET /api/v1/requests/<request_id>
```

Response:

```json
{
    "body": {
        "primary_poc": {
            "dodid_poc": "1234567890",
            "email_poc": "richard@promptworks.com",
            "fname_poc": "r",
            "lname_poc": "Howard"
        }
    },
    "creator": "164497f6-c1ea-4f42-a5ef-101da278c012",
    "id": "8b3e61c7-d727-4983-962d-1f273d1ae2ee",
    "status": "incomplete",
    "time_created": "2018-07-09T17:12:20.708670+00:00"
}
```

## Convenience / Utility Endpoints

### Status

Request:

```
GET /status
```

Response:

```
{
    "status": "ok"
}
```

### Root

Request:

```
GET /
```

Response:

```
Hello from requests-queue
```
