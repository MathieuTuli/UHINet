from flask import Flask, render_template, jsonify, request
from argparse import ArgumentParser
from pathlib import Path

import logging
import yaml

from ..components import LogLevel


parser = ArgumentParser(description=__doc__)
parser.add_argument(
    '-vv', '--very-verbose', action='store_true',
    dest='very_verbose',
    help="Set verbose. In effect, set --log-level to DEBUG.")
parser.add_argument(
    '-v', '--verbose', action='store_true',
    dest='verbose',
    help="Set verbose. In effect, set --log-level to INFO.")
parser.set_defaults(verbose=False)
parser.set_defaults(very_verbose=False)
parser.add_argument('--log-level', type=LogLevel.__getitem__,
                    default=LogLevel.INFO,
                    choices=LogLevel.__members__.values(),
                    dest='log_level',
                    help="Log level.")
parser.add_argument('--config', type=str,
                    default='instance/config.yaml',
                    dest='config_file',
                    help="YAML config file location.")

args = parser.parse_args()
if str(args.log_level) == 'DEBUG' or args.very_verbose:
    logging.root.setLevel(logging.DEBUG)
elif str(args.log_level) == 'INFO' or args.verbose:
    logging.root.setLevel(logging.INFO)
elif str(args.log_level) == 'WARNING':
    logging.root.setLevel(logging.WARNING)
elif str(args.log_level) == 'ERROR':
    logging.root.setLevel(logging.ERROR)
elif str(args.log_level) == 'CRITICAL':
    logging.root.setLevel(logging.CRITICAL)
else:
    logging.root.setLevel(logging.INFO)
    logging.warning(
        f"Frontend: Log level \"{args.log_level}\" unknown, defaulting" +
        " to INFO.")

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
