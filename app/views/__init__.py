from flask import Blueprint
from app.views.is_work import index_page
from app.views.tree import structure_page, tree_page
from app.views.task import task_page, task_manage_page

api_bp = Blueprint(
    'api', __name__,
    url_prefix='/api/',
    template_folder="templates"
)

api_bp.add_url_rule("/", view_func=index_page)
api_bp.add_url_rule("/tree", view_func=tree_page)
api_bp.add_url_rule("/structure", view_func=structure_page)
api_bp.add_url_rule("/task", view_func=task_page)
api_bp.add_url_rule("/task/manage", view_func=task_manage_page)
