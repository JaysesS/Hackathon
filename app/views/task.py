from flask.views import MethodView
from flask import jsonify


class TaskPresent(MethodView):

    methods = ['GET']

    def get(self):
        return jsonify(status=True, message="Task Is work!")


task_page = TaskPresent.as_view('task')
