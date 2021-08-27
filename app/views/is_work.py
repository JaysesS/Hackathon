from flask.views import MethodView
from flask import Blueprint, jsonify, g
from app.models import User

api_bp = Blueprint(
    'api', __name__,
    url_prefix='/api/',
    template_folder="templates"
)


class IsWorkView(MethodView):

    methods = ['GET']

    def get(self):
        print(g.session.query(User).all())
        return jsonify(status=True, message="Is work!")


index_page = IsWorkView.as_view('index')

api_bp.add_url_rule("/", view_func=index_page)
