from marshmallow import Schema, fields


class BaseNodeSchema(Schema):
    id = fields.Int(required=True, allow_none=False)


class PostNodeSchema(Schema):
    parent_id = fields.Int(required=True, allow_none=False)
    name = fields.Str(required=True, allow_none=False)

class NodeSchema(BaseNodeSchema):

    name = fields.Str(required=True, allow_none=False)
    path = fields.Str(required=True, allow_none=False)
    children = fields.List(fields.Nested(
        lambda: NodeSchema(), required=False), missing=[])


