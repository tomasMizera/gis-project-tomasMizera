from flask import Flask

import os


def create_app(_test_config=None):
    # create application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if _test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(_test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    @app.route('/hello')
    def hello():
        return "Hi, structured project!"

    return app
