from flask import Flask, render_template, jsonify, request
from argparse import _SubParsersAction, Namespace as APNamespace

from pathlib import Path
from components import *

import logging
import jinja2
import yaml


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
        logging.debug(f"Frontend: url specified: {url}")
        index = Path('map_io.html')
        return render_template(str(index), key=url)

    @app.route("/send_coordinates")
    def send_coordinates():
        coords_polygon = request.args.get('coords_polygon')
        coords_bound = request.args.get('coords_bound')
        print('\n')
        print(coords_polygon)
        print('\n')
        print(coords_bound)
        print('\n')
        image_name = str('image.png')
        return jsonify(image_name)
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
