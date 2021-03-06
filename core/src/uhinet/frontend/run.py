from argparse import _SubParsersAction, Namespace as APNamespace
from pathlib import Path

import logging
import jinja2
import yaml
import ast
import json

from flask import Flask, render_template, jsonify, request


from .components import Season, Orientation, GISLayer, Polygon, BuildingType
from ..backend.data.components import LatLon, BBox
from ..backend.requests import Requests


BACKEND = None
STATIC_DIR = Path('frontend/build/static').absolute()


def main(args: APNamespace):
    print("\n---------------------------------")
    print("UHINet Frontend Module")
    print("---------------------------------\n")
    build_dir = Path.cwd() / 'frontend/build'
    template_dir = build_dir / 'templates'
    static_dir = build_dir / 'static'
    assert(build_dir.exists())
    assert(template_dir.exists())
    assert(static_dir.exists())
    app = Flask(__name__, template_folder=str(
        template_dir), static_folder=str(static_dir))
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # loader = jinja2.ChoiceLoader([
    #     # app.jinja_loader,
    #     jinja2.FileSystemLoader(str(build_dir)),
    #     jinja2.FileSystemLoader(str(template_dir)),
    # ])
    # app.jinja_loader = loader

    @app.route("/", methods=["GET"])
    def map():
        # NOTE: All paths must be specified with relative path from top-level
        # module uhinet
        config_file = Path.cwd() / 'frontend/instance/config.yaml'
        if not config_file.exists():
            logging.error(
                f"Frontend: config file {config_file} was not found")
            return
        with config_file.open() as yaml_file:
            settings = yaml.load(yaml_file, Loader=yaml.FullLoader)
        url = "https://maps.googleapis.com/maps/api/js?" + \
            f"key={settings['google_maps_key']}" + \
            "&libraries=drawing&callback=initMap"
        global BACKEND
        # weights_path = Path(
        #     '/home/mat/work/U-of-T/capstone/uhinet/data/feb-12/' +
        #     '5-metres-80-range/pix2pix-training/summer/checkpoint')
        # weights_path = Path(
        #     '/home/mat/work/U-of-T/capstone/uhinet/data/feb-12/5-metres-v2/pix2pix-training/summer/checkpoint/')
        BACKEND = Requests(
            instance_id=str(settings['sentinel_hub_key']),
            # winter_weights_file=weights_path,
            # spring_weights_file=weights_path,
            # summer_weights_file=weights_path,
            # fall_weights_file=weights_path,
            flask_static_dir=STATIC_DIR,)
        # height_shp_file=Path(
        #     'data/shp/2019_height.shp'),
        # energy_shp_file=None)
        logging.debug(f"Frontend: url specified: {url}")
        index = Path('map.html')
        return render_template(str(index), key=url)

    @app.route("/send_coordinates")
    def send_coordinates():
        logging.info("UHINET Frontend: Send Coordinates.")
        coords_polygon = ast.literal_eval(request.args.get('coords_polygon'))
        coords_bound = ast.literal_eval(request.args.get('coords_bound'))
        colors = ast.literal_eval(request.args.get('colors'))
        polygon_color = ast.literal_eval(request.args.get('polygon_color'))
        # season = ast.literal_eval(request.args.get('season'))
        # height = float(ast.literal_eval(request.args.get('height')))
        # energy = float(ast. literal_eval(request.args.get('energy')))
        energy = 0.0

        lst_coords = []
        for coord in coords_polygon:
            lst_coords.append(LatLon(lat=coord['lat'], lon=coord['lng']))

        ''' Get Corresponding season '''
        def getSeason(season):
            if season == 'Spring':
                return Season.SPRING
            if season == 'Summer':
                return Season.SUMMER
            if season == 'Autumn':
                return Season.FALL
            if season == 'Winter':
                return Season.WINTER

        ''' Get Corresponding Building Type '''
        # TODO confirm this
        def getBuildingType(polygon_color, colors):
            if polygon_color == colors[0]:  # 0-->Residential
                return BuildingType.RESIDENTIAL
            elif polygon_color == colors[1]:  # 1-->Commercial
                return BuildingType.COMMERCIAL
            elif polygon_color == colors[2]:  # 2-->Parking Lot
                return BuildingType.PARKING_LOT
            else:  # 3-->Green Space
                return BuildingType.GREEN_SPACE

        # Polygon to use in the backend
        polygon = Polygon(coordinates=lst_coords,
                          viewing_window=BBox(top_left=LatLon(
                              lat=coords_bound['north'],
                              lon=coords_bound['west']),
                              bottom_right=LatLon(
                              lat=coords_bound['south'],
                              lon=coords_bound['east'])),
                          orientation=Orientation.CW,
                          building_type=getBuildingType(polygon_color, colors))
        # Orientation to be specified later

        '''
        Training and making predictions happen here
        '''

        # print(str(colors[0]))
        # print('\n')
        # print(type(colors[0]))
        # print('\n')
        # print(polygon_color in colors)

        '''
        GISlayer
        image_name = ... # image_name is the name of the predicted image
                     under /static/ folder
        '''
        global BACKEND
        layers = BACKEND.predict(
            polygon=polygon,
            season=Season.SUMMER,  # getSeason(season),
            height=0,
            energy=energy)
        image_names = [str(layers[0].image),  # Before image
                       str(layers[1].image),  # After image
                       str(layers[2].image)]  # Difference image
        coords_bound['north'] = layers[0].coordinates.top_left.lat
        coords_bound['west'] = layers[0].coordinates.top_left.lon
        coords_bound['south'] = layers[0].coordinates.bottom_right.lat
        coords_bound['east'] = layers[0].coordinates.bottom_right.lon
        assert((STATIC_DIR / image_names[0]).exists())
        assert((STATIC_DIR / image_names[1]).exists())
        assert((STATIC_DIR / image_names[2]).exists())
        logging.info("UHINET Frontend: Backend returned.")

        # image_name = str('image.png')
        # return jsonify(image_name)
        return jsonify(image_names=image_names, coords_bound=coords_bound)
    app.run(debug=args.verbose or args.very_verbose, host='127.0.0.1')


def args(sub_parser: _SubParsersAction) -> None:
    sub_parser.add_argument(
        '-vv', '--very-verbose', action='store_true',
        dest='very_verbose',
        help="Set flask debug mode")
    sub_parser.add_argument(
        '-v', '--verbose', action='store_true',
        dest='verbose',
        help="Set flask debug mode")
    sub_parser.set_defaults(verbose=False)
    sub_parser.set_defaults(very_verbose=False)
