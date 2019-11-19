import logging
from logging.config import dictConfig
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


DB_NAME = 'pdtdb'
DB_USERNAME = 'pdtuser'
DB_PASSWORD = 'pdtpassword'

conf = {
    "DEBUG": True,
    "DEVELOPMENT": True,
    "SQLALCHEMY_DATABASE_URI":
        f'postgres://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}',
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
logger = logging.getLogger(__name__)


def create_app():
    flask_app = Flask(__name__)
    flask_app.config = {**flask_app.config, **conf}
    # flask_app.register_blueprint(incidents_blueprint)
    # flask_app.url_map.strict_slashes = False

    # database engine
    db.init_app(flask_app)

    return flask_app


app = create_app()


@app.route('/', methods=['GET'])
def hello_world():
    logger.debug('Serving home response')
    return render_template('home.html')
    # db.engine.execute(
    # f'SELECT * FROM planet_osm_polygon where name=').first()[0]


@app.route('/get_view_locations', methods=['GET'])
def get_view_locations():

    points = [
        {
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': "Point",
                'coordinates': [13.854227716549076, 44.87547164896307]
            }
        },
        {
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': "Point",
                'coordinates': [13.588997396902641, 45.30831073392483]
            }
        }
    ]

    return jsonify(points)


if __name__ == '__main__':
    app.run()
