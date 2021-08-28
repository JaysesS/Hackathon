from flask import Blueprint
from app.views.is_work import index_page
from app.views.structure import structure_page, tree_page

api_bp = Blueprint(
    'api', __name__,
    url_prefix='/api/',
    template_folder="templates"
)

api_bp.add_url_rule("/", view_func=index_page)
api_bp.add_url_rule("/tree", view_func=tree_page)
api_bp.add_url_rule("/structure", view_func=structure_page)