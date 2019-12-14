from flask import Flask, render_template, jsonify, request
from argparse import ArgumentParser
from pathlib import Path

import logging
import yaml

from ..components import LogLevel


print("\n---------------------------------")
print("UHINet Frontend Module")
print("---------------------------------\n")


parser = ArgumentParser(description=__doc__)
parser.add_argument('--config', type=str,
                    default='instance/config.yaml',
                    dest='config_file',
                    help="YAML config file location.")

args = parser.parse_args()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def map():
    config_file = Path(args.config_file)
    if not config_file.exists():
        logging.error(
            f"Frontend: config file {args.config_file} was not found")
        return
    with config_file.open() as yaml_file:
        settings = yaml.load(yaml_file, Loader=yaml.FullLoader)
    url = f"https://maps.googleapis.com/maps/api/js?key={settings['key']}" + \
        "&libraries=drawing&callback=initMap"
    logging.debug(f"Frontend: url specified: {url}")
    return render_template('map_single_polygon.html', key=url)


@app.route("/send_coordinates")
def add_numbers():
    a = request.args.get('a')
    print('\n')
    print(a)
    print('\n')
    image_name = str('image.png')
    return jsonify(image_name)


if __name__ == '__main__':
    app.run(debug=True)
