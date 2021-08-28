from unittest import TestCase
import json
from sqlalchemy import func

from app.schemas.node import NodeSchema
from app.models import User, Node, get_session

class Test_DB(TestCase):


    @classmethod
    def setUpClass(cls):
        cls.session = get_session()
        cls.session.query(User).delete()
        cls.session.query(Node).delete()

    def fill_test(self):
        # 1
        cats = Node(name='cats')
        # 2
        lions = Node(name='lions', parent=cats)
        super_cats = Node(name='super_cats', parent=cats)
        # 4
        roman = Node(name='roman', parent=super_cats)

        tigers = Node(name='tigers', parent=lions)
        bengal_tigers = Node(name='bengal_tigers', parent=lions)

        self.session.add_all(
            [cats, lions, tigers, bengal_tigers, super_cats, roman])
        self.session.commit()

        tree = self.session.query(Node).all()
        self.assertEqual(len(tree), 6)

        tigers = self.session.query(Node).filter_by(name="tigers").first()
        self.assertEqual(tigers.parent.name, "lions")
        self.assertEqual([x.name for x in tigers.parent.children], [
            "tigers", "bengal_tigers"])

        third_layer = self.session.query(Node).filter(
            func.nlevel(Node.path) == 3).all()
        self.assertEqual([x.name for x in third_layer], [
            "tigers", "bengal_tigers", "roman"])

    def test_default(self):
        user = User(username = "Shrek")
        self.session.add(user)
        self.session.commit()
        get_user = self.session.query(User).filter_by(username="Shrek").first()
        self.assertEqual(user.username, get_user.username)

    def test_nodes(self):
        self.fill_test()
        node_schema = NodeSchema()
        root = self.session.query(Node).filter(
            func.nlevel(Node.path) == 1).all()

        print(json.dumps(Node.nodes_to_json(root), indent=4))



        # root_json = node_schema.dump(root, many=True)
        # print(json.dumps(root.to_json(), indent=4))
        # for node in root:
        #     print(node.children)
