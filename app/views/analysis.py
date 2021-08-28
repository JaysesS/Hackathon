from flask.views import MethodView
from flask import jsonify, request
from marshmallow.utils import pprint
from app.schemas.task import TaskAnalysisSchema, TaskSelectSchema
from app.models import Task


class AnalysisView(MethodView):

    methods = ['GET']

    def get(self):
        schema = TaskSelectSchema()
        analysis_schema = TaskAnalysisSchema()
        data = schema.load(request.args)
        task = Task.get_by_id(data.get('id'))
        if not task:
            return jsonify(status=False, message="Task not found")
        # task, assigner, active_task_count
        analysis_data = analysis_schema.dump(task)
        pprint(analysis_data)
        ##   analysis_data
        # 'assigner_name': 'Костя',
        # 'due_time': datetime.datetime(2021, 8, 29, 3, 47, 42),
        # 'end_time': datetime.datetime(2021, 8, 29, 1, 47, 42),
        # 'owner_name': 'Василёк',
        # 'priority': 80,
        # 'process_name': 'Разработка',
        # 'start_time': datetime.datetime(2021, 8, 28, 23, 47, 42),
        # 'task_name': 'Сделай гугл',
        # 'var_count': 228
        return jsonify(status=True, message="ok")


analysis_page = AnalysisView.as_view('analysis')
