from datetime import datetime, timedelta
from flask.views import MethodView
from flask import jsonify, request, g
from marshmallow.utils import pprint
from schemas.task import TaskAnalysisSchema, TaskSelectSchema
from schemas.user import UserAnalysisSchema
from models import Task, User
from analysis import model, scaler, helpers


class AnalysisView(MethodView):

    methods = ['GET']

    def get(self):
        schema = TaskSelectSchema()
        analysis_schema = TaskAnalysisSchema()
        user_analysis_schema = UserAnalysisSchema()
        data = schema.load(request.args)
        task = Task.get_by_id(data.get('id'))
        if not task:
            return jsonify(status=False, message="Task not found")
        analysis_data = analysis_schema.dump(task)
        users = g.session.query(User).all()
        model_result = []
        for user in users:
            if not analysis_data.task_name in helpers.users_pressets.get(user.name).keys():
                continue
            analysis_data.assigner = user.name
            processing_val = helpers.processing_val(
                [analysis_data], len(user.tasks_assign), model, scaler)
            predict = model.predict(processing_val)
            print("Username:", user.name, "Taks:", len(user.tasks_assign), "Work time:", timedelta(
                seconds=int(predict[0])), "Work time task:",analysis_data.due_time - analysis_data.start_time)
            model_result.append(dict(
                user=user,
                predict=int(predict[0])
            ))
        sort_result = sorted(model_result, key=lambda r:r['predict'])
        ranked = sort_result[:3]
        default = sort_result[3:]
        result = []
        for idx, u in enumerate(ranked, 1):
            data = user_analysis_schema.dump(u.get("user"))
            data["rank"] = idx
            result.append(data)
        result.extend([
            user_analysis_schema.dump(u.get("user")) for u in default
        ])
        return jsonify(status=True, users = result)


analysis_page = AnalysisView.as_view('analysis')
