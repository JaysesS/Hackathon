from typing import List, Optional
from flask import g
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Sequence, Index, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, remote, foreign, sessionmaker
from sqlalchemy import func
from sqlalchemy_utils import LtreeType, Ltree
from sqlalchemy_utils.types.ltree import LQUERY

import json
from schemas.user import UserChildrenSchema, UserSchema
from config import Config

Base = declarative_base()
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI,
                       **Config.SQLALCHEMY_ENGINE_OPTIONS)

id_seq = Sequence("nodes_id_seq")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, id_seq, primary_key=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    path = Column(LtreeType, nullable=False)

    parent = relationship(
        "User",
        primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
        backref="children",
        viewonly=True,
    )

    def __init__(self, name, position, parent=None):
        _id = engine.execute(id_seq)
        self.id = _id
        self.name = name
        self.position = position
        ltree_id = Ltree(str(_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id

    __table_args__ = (Index("ix_nodes_path", path, postgresql_using="gist"),)

    def show_json(self):
        schema = UserChildrenSchema()
        print(json.dumps(schema.dump(self), indent=4))

    def to_json(self):
        schema = UserChildrenSchema()
        return schema.dump(self)

    def delete(self):
        g.session.delete(self)
        g.session.commit()

    @staticmethod
    def nodes_to_json(nodes: List["User"]) -> dict:
        schema = UserChildrenSchema()
        return schema.dump(nodes, many=True)

    @classmethod
    def get_flat_list(cls, list = None) -> List[dict]:
        schema = UserSchema()
        return schema.dump(g.session.query(User).all(), many=True)

    @classmethod
    def get_by_level(cls, level: int) -> List["User"]:
        return g.session.query(cls).filter(
            func.nlevel(cls.path) == level).all()

    @classmethod
    def get_by_id(cls, id: int) -> "User":
        return g.session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_by_name(cls, name: int) -> "User":
        return g.session.query(cls).filter_by(name=name).first()

    @classmethod
    def insert_node(cls, parent_id: int, name: str, position: str) -> Optional["User"]:
        parent = cls.get_by_id(parent_id)
        if parent:
            node = cls(name=name, position=position, parent=parent)
            g.session.add(node)
            g.session.commit()
            return node
        return None

    def __repr__(self):
        return 'User({})'.format(self.name)


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False, unique=False)
    process_name = Column(String, nullable=False, unique=False)

    start_time = Column(Integer, nullable=False)
    due_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=True)
    priority = Column(Integer, nullable=False)
    var_count = Column(Integer, nullable=False)

    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    assigner_id = Column(Integer, ForeignKey('user.id'), nullable=True)

    owner = relationship(User, foreign_keys=[owner_id], backref='tasks_own')
    assigner = relationship(
        User, foreign_keys=[assigner_id], backref='tasks_assign')

    started = Column(Boolean, server_default='t', default=False)
    was_started = Column(Boolean, server_default='t', default=False)

    def __repr__(self) -> str:
        return f"Task({self.process_name} -> {self.name})"

    def is_started(self):
        return self.started


    def change_state(self, state):
        if state == "start":
            return self.start()
        return self.stop()

    def start(self):
        if not self.was_started:
            self.started = True
            self.was_started = True
            g.session.commit()
            return self
        # TASK WAS STARTED BEFORE
        return None

    def stop(self):
        if self.started:
            self.started = False
            self.end_time = datetime.now().timestamp()
            g.session.commit()
            return self
        # STOP STOPED TASK??)
        return None

    @classmethod
    def get_by_id(cls, id: int) -> "Task":
        return g.session.query(cls).filter_by(id=id).first()


def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

# To create a tree like the example shown
# at the top of this post:
# cats = Node("cats")
# big = Node("big", parent=cats)
# small = Node("small", parent=cats)
# wild = Node("wild", parent=small)
# domestic = Node("domestic", parent=small)
# session.add_all((cats, big, small, wild, domestic))
# for big_cat in ("lion", "tiger", "jaguar"):
#     session.add(Node(big_cat, parent=big))
# for small_wildcat in ("ocelot", "bobcat"):
#     session.add(Node(small_wildcat, parent=wild))
# for domestic_cat in ("persian", "bengal", "shorthair"):
#     session.add(Node(domestic_cat, parent=domestic))

# session.flush()

# To retrieve a whole subtree:
# whole_subtree = session.query(Node).filter(
#     Node.path.descendant_of(domestic.path)).all()
# print('Whole subtree:', whole_subtree)
# [domestic, persian, bengal, shorthair]

# Get only the third layer of nodes:
# third_layer = session.query(Node).filter(func.nlevel(Node.path) == 3).all()
# print('Third layer:', third_layer)
# [wild, domestic, lion, tiger, jaguar]

# Get all the siblings of a node:
# shorthair = session.query(Node).filter_by(name="shorthair").one()
# siblings = session.query(Node).filter(
#     # We can use Python's slice notation on ltree paths:
#     Node.path.descendant_of(shorthair.path[:-1]),
#     func.nlevel(Node.path) == len(shorthair.path),
#     Node.id != shorthair.id,
# ).all()
# print('Siblings of shorthair:', siblings)
# [persian, bengal]

# Using an LQuery to get immediate children of two parent nodes at different depths:
# query = "*.%s|%s.*{1}" % (big.id, wild.id)
# lquery = expression.cast(query, LQUERY)
# immediate_children = session.query(Node).filter(Node.path.lquery(lquery)).all()
# print('Immediate children of big and wild:', immediate_children)
# [lion, tiger, ocelot, jaguar, bobcat]
