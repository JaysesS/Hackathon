from typing import List
from marshmallow import Schema, fields, EXCLUDE

from pprint import pprint


class PostUserSchema(Schema):
    parent_id = fields.Int(required=True, allow_none=False)
    name = fields.Str(required=True, allow_none=False)
    position = fields.Str(required=True, allow_none=False)


class BaseUserSchema(Schema):
    id = fields.Int(required=True, allow_none=False)


class UserSchema(BaseUserSchema):

    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True, allow_none=False)
    path = fields.Str(required=True, allow_none=False)
    position = fields.Str(required=True, allow_none=False)

class UserChildrenSchema(UserSchema):

    children = fields.List(fields.Nested(
        lambda: UserChildrenSchema(), required=False), missing=[])
