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

    # database engine
    db.init_app(flask_app)

    return flask_app


app = create_app()


@app.route('/', methods=['GET'])
def hello_world():
    logger.debug('Serving home response')
    return render_template('home.html')


@app.route('/get_view_locations', methods=['GET'])
def get_view_locations():

    beaches = db.engine.execute(
        """
        with beaches as (
            select name, ST_X(st_astext(st_transform(way, 4326))) as longitude,
                ST_Y(st_astext(st_transform(way, 4326))) as latitude
            from planet_osm_point
            where "natural" = 'beach'
            union all
            select name, st_x(st_astext(st_centroid(st_transform(way, 4326)))) as longitude,
                st_y(st_astext(st_centroid(st_transform(way, 4326)))) as latitude
            from planet_osm_polygon
            where "natural" = 'beach'
        )

        select *
        from beaches;
        """
    )

    points = [
        {'type': 'Feature',
         'properties': {},
         'geometry': {
             'type': "Point",
             'coordinates': [beach[1], beach[2]]
         }} for beach in beaches
    ]

    return jsonify([points[0]])

# icon urls https://icons8.com/icon/set/pin/metro


@app.route('/get_temp_view', methods=['GET'])
def get_temp_view():

    beaches = db.engine.execute(
        """
        with beaches as (
            select name, ST_X(st_astext(st_transform(way, 4326))) as longitude,
                ST_Y(st_astext(st_transform(way, 4326))) as latitude
            from planet_osm_point
            where "natural" = 'beach'
            union all
            select name, st_x(st_astext(st_centroid(st_transform(way, 4326)))) as longitude,
                st_y(st_astext(st_centroid(st_transform(way, 4326)))) as latitude
            from planet_osm_polygon
            where "natural" = 'beach'
        )

        select name, longitude - 0.057635373 as longitude, latitude
        from beaches;
        """
    )

    points = [
        {'type': 'Feature',
         'properties': {},
         'geometry': {
             'type': "Point",
             'coordinates': [beach[1], beach[2]]
         }} for beach in beaches
    ]

    return jsonify([points[0]])


@app.route('/get_down_view', methods=['GET'])
def get_down_view():

    beaches = db.engine.execute(
        """
        with beaches as (
            select name, ST_X(st_astext(st_transform(way, 4326))) as longitude,
                ST_Y(st_astext(st_transform(way, 4326))) as latitude
            from planet_osm_point
            where "natural" = 'beach'
            union all
            select name, st_x(st_astext(st_centroid(st_transform(way, 4326)))) as longitude,
                st_y(st_astext(st_centroid(st_transform(way, 4326)))) as latitude
            from planet_osm_polygon
            where "natural" = 'beach'
        )

        select name, longitude - 0.057635373 as longitude, latitude - 0.02385071216053 as latitude
        from beaches;
        """
    )

    points = [
        {'type': 'Feature',
         'properties': {},
         'geometry': {
             'type': "Point",
             'coordinates': [beach[1], beach[2]]
         }} for beach in beaches
    ]

    return jsonify([points[0]])


@app.route('/get_up_view', methods=['GET'])
def get_up_view():

    beaches = db.engine.execute(
        """
        with beaches as (
            select name, ST_X(st_astext(st_transform(way, 4326))) as longitude,
                ST_Y(st_astext(st_transform(way, 4326))) as latitude
            from planet_osm_point
            where "natural" = 'beach'
            union all
            select name, st_x(st_astext(st_centroid(st_transform(way, 4326)))) as longitude,
                st_y(st_astext(st_centroid(st_transform(way, 4326)))) as latitude
            from planet_osm_polygon
            where "natural" = 'beach'
        )

        select name, longitude - 0.057635373 as longitude, latitude + 0.02385071216053 as latitude
        from beaches;
        """
    )

    points = [
        {'type': 'Feature',
         'properties': {},
         'geometry': {
             'type': "Point",
             'coordinates': [beach[1], beach[2]]
         }} for beach in beaches
    ]

    return jsonify([points[0]])


def parse(x):
    l = list(map(lambda q: q.split(' '), x[1].replace('POLYGON', '').replace('((', '').replace('))', '').split(','))) 
    return l


@app.route('/get_polygons', methods=['GET'])
def get_polygons():

    beaches = db.engine.execute(
        """
        with beaches as (
            select name, ST_X(st_astext(st_transform(way, 4326))) as longitude,
                ST_Y(st_astext(st_transform(way, 4326))) as latitude
            from planet_osm_point
            where "natural" = 'beach'
            union all
            select name, st_x(st_astext(st_centroid(st_transform(way, 4326)))) as longitude,
                st_y(st_astext(st_centroid(st_transform(way, 4326)))) as latitude
            from planet_osm_polygon
            where "natural" = 'beach'
        )

        select name, st_astext(st_makepolygon(st_makeline(ARRAY[
            st_point(longitude, latitude),
            st_point(longitude - 0.057635373, latitude - 0.02385071216053),
            st_point(longitude - 0.057635373, latitude + 0.02385071216053),
            st_point(longitude, latitude)
            ]))) as polygon
        from beaches;
        """
    )
    coords = [parse(co) for co in beaches]

    print(coords)

    points = [
        {'type': 'Feature',
         'properties': {},
         'geometry': {
             'type': "Polygon",
             'coordinates': view
         }} for view in coords
    ]

    return jsonify([points[0]])


if __name__ == '__main__':
    app.run()
