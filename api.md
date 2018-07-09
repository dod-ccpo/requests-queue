# Requests Queue API

## Requests

### Create request

Create a new JEDI request.

```
POST /api/v1/requests

{
    "creator_id": "",
    "request": {

    }
}

```

### Update request

Update an existing request.

```
PATCH /api/v1/requests/<request_id>

{
    "creator_id": "",
    "request": {

    }
}
```

### Get requests

Get a list of a user's requests.

```
GET /api/v1/users/<user_id>/requests
```

### Get request

Get a user's request.

```
GET /api/v1/users/<user_id>/requests/<request_id>
```
