from flask import Flask, render_template, jsonify, request
from argparse import _SubParsersAction, Namespace as APNamespace

from pathlib import Path

import logging
import yaml


def main(args: APNamespace):
    print("\n---------------------------------")
    print("UHINet Frontend Module")
    print("---------------------------------\n")
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def map(config_file: Path):
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
        index = Path.cwd() / 'app/static/index.html'
        return render_template(str(index), key=url)

    @app.route("/send_coordinates")
    def add_numbers():
        a = request.args.get('a')
        print('\n')
        print(a)
        print('\n')
        image_name = str('image.png')
        return jsonify(image_name)
    app.run(debug=True, host='127.0.0.1')


def args(parser: _SubParsersAction) -> None:
    parser.add_argument('--config', type=str,
                        default='instance/config.yaml',
                        dest='config_file',
                        help="YAML config file location.")
