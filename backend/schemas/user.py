from typing import List
from marshmallow import Schema, fields, EXCLUDE

from pprint import pprint

from marshmallow.decorators import post_dump


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
    tasks_assign = fields.List(fields.Raw, required=True, allow_none=False, dump_only=True)

    @post_dump
    def _count_tasks(self, data, **kwargs):
        data["task_count"] = len(data["tasks_assign"])
        del data["tasks_assign"]
        return data

class UserChildrenSchema(UserSchema):

    children = fields.List(fields.Nested(
        lambda: UserChildrenSchema(), required=False), missing=[])
