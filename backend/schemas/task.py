from datetime import datetime
from marshmallow import Schema, fields, validate
from marshmallow.decorators import post_dump, post_load
from models import User
from analysis.dto import TaskRawData


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


class TaskSelectSchema(Schema):

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


class TaskAnalysisSchema(Schema):

    task_name = fields.Str(required=True, allow_none=False,
                           attribute="name", dump_only=True)
    process_name = fields.Str(required=True, allow_none=False)
    start_time = fields.Int(required=True, allow_none=False)
    due_time = fields.Int(required=True, allow_none=False)
    end_time = fields.Int(required=False, allow_none=True)
    priority = fields.Int(required=True, allow_none=False)
    var_count = fields.Int(required=True, allow_none=False)
    owner_id = fields.Int(required=True, allow_none=False)
    assigner_id = fields.Int(required=False, allow_none=True)

    @post_dump
    def _post_dump(self, data, **kwargs):
        owner = User.get_by_id(data["owner_id"])
        assigner = User.get_by_id(data["assigner_id"])
        if owner and assigner:
            data["owner"] = owner.name
            data["assigner"] = assigner.name
            del data["owner_id"]
            del data["assigner_id"]
        if data['start_time'] and data['due_time']:
            data['start_time'] = datetime.fromtimestamp(data['start_time'])
            data['due_time'] = datetime.fromtimestamp(data['due_time'])
        if data['end_time']:
            data['end_time'] = datetime.fromtimestamp(data['end_time'])
        data['is_bind'] = True
        return TaskRawData(**data)
