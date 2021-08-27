from flask import Flask, g


class DbMiddleware:
    def __init__(self, sessionmaker):
        self.sessionmaker = sessionmaker

    def open(self):
        session = self.sessionmaker()
        g.session = session

    def close(self, *_args, **_kwargs):
        g.session.close()

    def register(self, app: Flask):
        app.before_request(self.open)
        app.teardown_appcontext(self.close)
