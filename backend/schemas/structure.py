from marshmallow import Schema, fields


class StructureSchema(Schema):

    flat = fields.Bool(required=False, allow_none=True)
