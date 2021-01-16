from flask import Flask


def init_app():
    app = Flask(__name__)

    with app.app_context():
        from . import routes

        from .dashapp.app import init_dash

        init_dash(app)
        return app
