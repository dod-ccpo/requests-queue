from marshmallow_sqlalchemy import ModelSchema
from requests_queue.models.request import Request


class RequestSerializer(ModelSchema):
    class Meta:
        model = Request
