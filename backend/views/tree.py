from flask.views import MethodView
from flask import jsonify, request

from schemas.user import BaseUserSchema, PostUserSchema
from schemas.structure import StructureSchema
from models import User


class StructurePresent(MethodView):

    methods = ['GET']

    def get(self):
        schema = StructureSchema()
        data = schema.load(request.args)
        if data.get("flat"):
            return jsonify(status=True, users=User.get_flat_list())
        return jsonify(status=True, tree=User.nodes_to_json(User.get_by_level(1)))


class TreeManage(MethodView):

    methods = ['GET', 'POST', 'DELETE']

    def get(self):
        schema = BaseUserSchema()
        data = schema.load(request.args)
        node = User.get_by_id(data.get("id")).to_json()
        return jsonify(status=True, node=node)

    def post(self):
        schema = PostUserSchema()
        data = schema.load(request.get_json())
        node = User.insert_node(**data)
        if node:
            return jsonify(status=True, node=node.to_json())
        return jsonify(status=False, message='Probably parent not found ;c')
    
    def delete(self):
        schema = BaseUserSchema()
        data = schema.load(request.args)
        node = User.get_by_id(data.get("id"))
        if not node:
            return jsonify(status=False, message='Node not found ;c')
        if len(node.tasks_own) != 0 and len(node.tasks_assign) != 0:
            return jsonify(status=False, message='Освободите человека от задач прежде чем удалять!')
        node.delete()
        return jsonify(status=True, node_id=data.get("id"), message='Node was removed')


structure_page = StructurePresent.as_view('structure')
tree_page = TreeManage.as_view('tree')
