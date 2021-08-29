from functools import wraps
from unittest import TestCase
from flask.globals import g
from datetime import datetime, timedelta
from sqlalchemy import func
from app import create_app
import json

from models import User, Task, get_session, Base, engine


class Test_DB(TestCase):

    @classmethod
    def setUpClass(cls):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        cls.session = get_session()
        cls.app = create_app()

    def mock_g(func):
        @wraps(func)
        def _wrapper(self, *args, **kwargs):
            with self.app.test_request_context():
                g.session = self.session
                result = func(self, *args, **kwargs)
            return result
        return _wrapper

    def fill_test_users(self):
        self.session.query(User).delete()
        # 1
        director = User(name='Василёк', position="Директор")
        # 2
        frontend = User(name='Петя',
                        position="Фронт", parent=director)
        backend = User(name='Глеб',
                       position="Архитектор", parent=director)
        market = User(name='Соня',
                      position="Маркетинг", parent=director)
        devops = User(name='Ванёк',
                      position="devOps", parent=director)
        design = User(name='Ден',
                      position="Десигн", parent=director)
        # 3
        backend2 = User(name='Игорь',
                        position="Писатель питона", parent=backend)
        tester = User(name='Абстрактный тестировщик',
                      position="Тестер питона", parent=backend)
        frontend2 = User(name='Еремей',
                         position="Фронт", parent=frontend)
        # 4
        backend3 = User(name='Абстрактный джун питона',
                        position="Писатель питона", parent=backend2)
        frontend3 = User(name='Абстрактный джун JS\'a',
                         position="Фронт", parent=frontend2)
        devops2 = User(name='Абстрактный джун devopa',
                      position="devOPs", parent=devops)

        self.session.add_all(
            [director, backend, backend2, frontend, frontend2, market, tester, devops, design, backend3, frontend3, devops2])
        self.session.commit()

    @mock_g
    def fill_test_tasks(self):
        director = User.get_by_name("Василёк")
        igor_backend = User.get_by_name("Игорь")
        gleb = User.get_by_name("Глеб")
        eremey = User.get_by_name("Еремей")
        petr = User.get_by_name("Петя")
        sonya = User.get_by_name("Соня")
        denis = User.get_by_name("Ден")
        task1 = Task(
            name="Фикс чего-то там",
            process_name="Поддержка",
            owner_id=director.id,
            assigner_id=igor_backend.id,
            start_time=datetime.now().timestamp(),
            due_time=(datetime.now() + timedelta(hours=5)).timestamp(),
            end_time=(datetime.now() + timedelta(hours=4)).timestamp(),
            priority=8,
            var_count=2
        )
        task2 = Task(
            name="Сделай гугл",
            process_name="Разработка",
            owner_id=director.id,
            assigner_id=gleb.id,
            start_time=datetime.now().timestamp(),
            due_time=(datetime.now() + timedelta(hours=4)).timestamp(),
            end_time=(datetime.now() +
                      timedelta(hours=2)).timestamp(),
            priority=6,
            var_count=228
        )
        task3 = Task(
            name="Перепиши весь десигн",
            process_name="Поддержка",
            owner_id=petr.id,
            assigner_id=eremey.id,
            start_time=datetime.now().timestamp(),
            due_time=(datetime.now() + timedelta(hours=8)).timestamp(),
            end_time=(datetime.now() +
                      timedelta(hours=5, minutes=30)).timestamp(),
            priority=9,
            var_count=100
        )
        task4 = Task(
            name="проверка склада",
            process_name="Заказ товара",
            owner_id=denis.id,
            assigner_id=sonya.id,
            start_time=datetime.now().timestamp(),
            due_time=(datetime.now() + timedelta(hours=1)).timestamp(),
            end_time=(datetime.now() +
                      timedelta(minutes=30)).timestamp(),
            priority=9,
            var_count=1
        )
        task5 = Task(
            name="Оформить заявку",
            process_name="закупка",
            owner_id=denis.id,
            assigner_id=sonya.id,
            start_time=datetime.now().timestamp(),
            due_time=(datetime.now() + timedelta(hours=2)).timestamp(),
            end_time=(datetime.now() +
                      timedelta(minutes=30)).timestamp(),
            priority=5,
            var_count=1
        )
        self.session.add_all([task1, task2, task3, task4, task5])
        self.session.commit()

    @mock_g
    def test_nodes(self):
        self.fill_test_users()
        root = User.get_by_level(1)
        # print(json.dumps(User.nodes_to_json(root), indent=4, ensure_ascii=False))
        root = User.get_flat_list()
        # print(json.dumps(root, indent=4, ensure_ascii=False))
        # print(root)

    @mock_g
    def test_task(self):
        self.fill_test_users()
        self.fill_test_tasks()
        tasks = self.session.query(Task).all()
        self.assertEqual(len(tasks), 5)
        director = User.get_by_name("Василёк")
        self.assertEqual(len(director.tasks_assign), 0)
        self.assertEqual(len(director.tasks_own), 2)
        igor_backend = User.get_by_name("Игорь")
        self.assertEqual(len(igor_backend.tasks_assign), 1)
        self.assertEqual(len(igor_backend.tasks_own), 0)
