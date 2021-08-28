from flask.views import MethodView
from flask import jsonify, g
from app.models import User


class IsWorkView(MethodView):

    methods = ['GET']

    def get(self):
        return jsonify(status=True, message="Is work!")


index_page = IsWorkView.as_view('index')