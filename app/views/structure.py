from flask.views import MethodView
from flask import jsonify, request

from app.schemas.node import BaseNodeSchema, PostNodeSchema
from app.models import Base, User, Node


class WorkerPresent(MethodView):

    methods = ['GET']

    def get(self):
        root = Node.get_by_level(1)
        tree = Node.nodes_to_json(root)
        return jsonify(status=True, tree=tree)

class TreeManage(MethodView):

    methods = ['GET', 'POST']

    def get(self):
        schema = BaseNodeSchema()
        data = schema.load(request.args)
        node = Node.get_by_id(data.get("id")).to_json()
        return jsonify(status=True, node=node)

    def post(self):
        schema = PostNodeSchema()
        data = schema.load(request.get_json())
        node = Node.insert_node(**data)
        if node:
            return jsonify(status=True, node=node.to_json())
        return jsonify(status=False, message='Probably parent not found ;c')


structure_page = WorkerPresent.as_view('structure')
tree_page = TreeManage.as_view('tree')
