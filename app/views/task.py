from flask.globals import request
from flask.views import MethodView
from flask import jsonify, g
from app.models import Task
from app.schemas.task import TaskSchema, TaskFilterSchema, TaskDeleteSchema, TaskActionSchema


class TaskPresent(MethodView):

    methods = ['GET', 'POST', 'DELETE']

    def get(self):
        filter_schema = TaskFilterSchema()
        task_schema = TaskSchema()
        filter = filter_schema.load(request.args)
        if not filter.get('args'):
            data = g.session.query(Task).all()
        else:
            data = g.session.query(Task).filter_by(
                **filter.get("filter")).all()
        tasks = task_schema.dump(data, many=True)
        return jsonify(status=True, tasks = tasks)

    def post(self):
        task_schema = TaskSchema()
        data = task_schema.load(request.get_json())
        task = Task(**data)
        g.session.add(task)
        g.session.commit()
        return jsonify(status=True, task_id=task.id)

    def delete(self):
        schema = TaskDeleteSchema()
        data = schema.load(request.args)
        task = Task.get_by_id(data.get('id'))
        if task:
            g.session.delete(task)
            g.session.commit()
            return jsonify(status=True, task_id=task.id, message="Was removed")
        return jsonify(status=False, task_id=data.get('id'), message="Not found")


class TaskManage(MethodView):

    methods = ['POST']

    def post(self):
        schema = TaskActionSchema()
        data = schema.load(request.get_json())
        if data.get("args"):
            task = Task.get_by_id(data.get("id"))
            task_schema = TaskSchema()
            action = data.get("action")
            state = action.get("state")
            if state:
                check = task.change_state(state)
                if not check:
                    return jsonify(status=False, message = "Problem with task state, task already started or was ended before!")
            for key, value in action.items():
                task.__setattr__(key, value)
                g.session.commit()
            task_json = task_schema.dump(task)
            return jsonify(status=True, task=task_json)
        return jsonify(status=False, message="Actions was empty!")

task_page = TaskPresent.as_view('task')
task_manage_page = TaskManage.as_view('task_manage')
