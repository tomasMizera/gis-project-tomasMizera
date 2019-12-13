import logging
from logging.config import dictConfig
from flask import Flask, jsonify, render_template, request
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


DB_NAME = 'pdtdb'
DB_USERNAME = 'pdtuser'
DB_PASSWORD = 'pdtpassword'

conf = {
    "DEBUG": True,
    "DEVELOPMENT": True,
    "SQLALCHEMY_DATABASE_URI":
        f'postgres://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}',
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "JSON_SORT_KEYS": False
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


# ROUTES ----------------------------->

def build_geojson_feature_c(_response, _layer_id):
    elements = [json.loads(res[0]) for res in _response]

    GeoJSON = {
        'id': _layer_id,
        'type': 'FeatureCollection',
        'features': list(map(lambda x: {
            'type': 'Feature',
            'properties': {},
            'geometry': x
        }, elements))
    }
    return GeoJSON


@app.route('/', methods=['GET'])
def hello_world():
    logger.debug('Serving home response')
    return render_template('home.html')


@app.route('/api/get_beaches', methods=['GET'])
def get_beaches():
    beaches = db.engine.execute(
        """
        select st_asgeojson(beach_pos)
        from beach_view;
        """
    )

    return jsonify(build_geojson_feature_c(beaches, 'beaches'))


def parse_polygon(x):
    return [list(map(
        lambda q: q.split(' '),
        x[1].replace('POLYGON', '')
            .replace('((', '')
            .replace('))', '')
            .split(','))
    )]


@app.route('/api/get_sight_views', methods=['GET'])
def get_polygons():

    views_from_coast = db.engine.execute(
        """
        with beaches as (
            select name, ST_X(st_astext(st_transform(way, 4326))) as longitude,
                ST_Y(st_astext(st_transform(way, 4326))) as latitude
            from planet_osm_point
            where "natural" = 'beach'
            union all
            select name,
                st_x(st_astext(st_centroid(st_transform(way, 4326))))
                  as longitude,
                st_y(st_astext(st_centroid(st_transform(way, 4326))))
                  as latitude
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
    coords = [parse_polygon(co) for co in views_from_coast]

    GeoJSON = {
        'type': 'Feature',
        'geometry': {
            'type': 'MultiPolygon',
            'coordinates': coords
        }
    }

    return jsonify(GeoJSON)


@app.route('/api/get_coastline', methods=['GET'])
def get_coastline():
    coastlines = db.engine.execute(
        """
        select st_asgeojson(st_transform(spatial_coast.way, 4326))
        from spatial_coast;
        """
    )

    return jsonify(build_geojson_feature_c(coastlines, 'coastline'))


@app.route('/api/get_intersections', methods=['GET'])
def get_test():

    willing_walking = request.args.get('walking_distance', 0.05)

    q = text("""with intersecting as (
        select distinct beach.osm_id
        from beach_view beach
        cross join spatial_coast coast
        where st_intersects(beach.sight_way, coast.way) and
            st_maxdistance(beach.beach_pos, coast.way) > :walking_distance
    )
    select st_asgeojson(beach.sight_way)
    from beach_view beach
    where beach.osm_id not in (select * from intersecting);""")

    intersected_views = db.engine.execute(q, walking_distance=willing_walking)

    return jsonify(build_geojson_feature_c(intersected_views, 'intersections'))
