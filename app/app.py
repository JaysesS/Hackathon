from flask import Flask
from sqlalchemy.orm import sessionmaker

from app.middleware import DbMiddleware
from app.models import engine, Base
from app.config import Config
from app.views.is_work import api_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    DbMiddleware(sessionmaker(bind=engine)).register(app)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    app.register_blueprint(api_bp)

    return app
