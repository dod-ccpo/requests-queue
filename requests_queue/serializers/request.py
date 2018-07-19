from marshmallow import Schema, fields


class RequestSerializer(Schema):
    id = fields.UUID()
    creator = fields.UUID()
    time_created = fields.DateTime()
    body = fields.Dict()
    status = fields.String()
    action_requred_by = fields.String()
