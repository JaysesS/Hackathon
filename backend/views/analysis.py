from datetime import datetime, timedelta
from flask.views import MethodView
from flask import jsonify, request, g
from marshmallow.utils import pprint
from schemas.task import TaskAnalysisSchema, TaskSelectSchema
from models import Task, User
import numpy as np
from analysis import model, scaler, helpers


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
        users = g.session.query(User).all()
        for user in users:
            analysis_data.assigner = user.name
            processing_val = helpers.processing_val(
                [analysis_data], len(user.tasks_assign), model, scaler)
            predict = model.predict(processing_val)
            print("Username:", user.name, "Taks:", len(user.tasks_assign), "Work time:", timedelta(
                seconds=int(predict[0])), "Work time task:",analysis_data.due_time - analysis_data.start_time)
        return jsonify(status=True, message="ok")


analysis_page = AnalysisView.as_view('analysis')
