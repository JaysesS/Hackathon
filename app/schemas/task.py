from marshmallow import Schema, fields, validate
from marshmallow.decorators import post_dump, post_load


class TaskSchema(Schema):

    id = fields.Int(required=True, allow_none=False, dump_only = True)
    name = fields.Str(required=True, allow_none=False)
    process_name = fields.Str(required=True, allow_none=False)
    start_time = fields.Int(required=True, allow_none=False)
    due_time = fields.Int(required=True, allow_none=False)
    end_time = fields.Int(required=False, allow_none=True, dump_only=True)
    priority = fields.Int(required=True, allow_none=False)
    var_count = fields.Int(required=True, allow_none=False)
    owner_id = fields.Int(required=True, allow_none=False)
    assigner_id = fields.Int(required=False, allow_none=True)
    started = fields.Bool(required=False, allow_none=True, dump_only=True)


class TaskDeleteSchema(Schema):

    id = fields.Int(required=True, allow_none=False)

class TaskActionSchema(Schema):

    id = fields.Int(required=True, allow_none=False)
    state = fields.Str(required=False, allow_none=True,
                        validate=validate.OneOf(choices=["start", 'stop']))
    assigner_id = fields.Int(required=False, allow_none=True)
    owner_id = fields.Int(required=False, allow_none=True)

    @post_load
    def _post_load(self, data, **kwargs):
        result = {}
        result['id'] = data.get("id")
        del data["id"]
        result['action'] = {}
        result['args'] = False
        for key, val in data.items():
            if val is not None:
                result['action'][key] = val
        if len(result['action']) != 0:
            result["args"] = True
        return result

class TaskFilterSchema(Schema):

    id = fields.Int(required=False, allow_none=True)
    process_name = fields.Str(required=False, allow_none=True)
    owner_id = fields.Int(required=False, allow_none=True)
    assigner_id = fields.Int(required=False, allow_none=True)
    started = fields.Bool(required=False, allow_none=True)

    @post_load
    def _post_load(self, data, **kwargs):
        result = {}
        result['filter'] = {}
        result['args'] = False
        for key, val in data.items():
            if val is not None:
                result['filter'][key] = val
        if len(result['filter']) != 0:
            result["args"] = True
        return result
