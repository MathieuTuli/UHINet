"""
UHINet Data Module
"""
from argparse import _SubParsersAction, Namespace as APNamespace

from pathlib import Path

import logging
import signal
import sys

from .download_landsat import download_landsat_from_file
from .sentinel_hub import SentinelHubAccessor
from ..file_manager import file_exists


def control_c_handler(_signal, frame):
    print("\n---------------------------------")
    print("Data Shell: Ctrl-C. Shutting Down.")
    print("---------------------------------")
    sys.exit(0)


def main(args: APNamespace):
    print("\n---------------------------------")
    print("UHINet Data Module")
    print("---------------------------------\n")

    signal.signal(signal.SIGINT, control_c_handler)
    if args.data_source.lower() == 'landsat':
        logging.warning(
            "Data Shell: Currently, only landsat downloads from a " +
            "shopping list file are permitted")
        shopping_list_path = Path(args.shopping_list)
        instance_id_path = Path(args.instance_id)
        if file_exists(shopping_list_path) and file_exists(instance_id_path):
            logging.info("Data Shell: Downloading landsat from shopping " +
                         f"list found at \"{args.shopping_list}\"")

            with instance_id_path.open() as f:
                instance_id = f.read().strip()

            sentinelhub_accessor = SentinelHubAccessor(instance_id)
            download_landsat_from_file(
                sentinelhub_accessor, shopping_list_path, Path(args.save_to))

    else:
        logging.error(
            f"Data Shell: Data source \"{args.data_source.lower()}\" unknown.")
        sys.exit(0)


def args(sub_parser: _SubParsersAction) -> None:
    sub_parser.add_argument('--data-source', type=str.lower,
                            dest='data_source',
                            choices=['landsat'],
                            required=True,
                            help="Required. Data source for download.")
    sub_parser.add_argument(
        '--instance-id', type=str,
        default='instance_id.txt',
        dest='instance_id',
        help="Default: instance_id.txt. File name of instance id for \n" +
        "data-set-specific API Accessor")
    sub_parser.add_argument(
        '--shopping-list', type=str,
        default='shopping_list.json',
        dest='shopping_list',
        help="Default: shopping_list.json. File name of settings and \n" +
        "API demands for data-set-specific download.\n" +
        "See \"core/src/uhinet/backend/data/shopping_list_example.txt\"\n" +
        "for an example.\n"
        f"Valid keys are as follows:\n" +
        "    - centers: a dict of centers coordinates and id. Subkeys are \n" +
        "            {name, lat, lon}.\n" +
        "    - year_from: Start date to grab data from.\n" +
        "    - year_to: Start date to grab data to.\n" +
        "    - image_size: Tuple of image size in format (height, width)\n" +
        "    - layers: List of layers from Landsat. Valid = [LST, RGB]\n" +
        "    - cloud_coverage_percentage: Float betwen [0, 1] for \n" +
        "            cloud coverage percentag\n" +
        "    - spatial_resolution: Spatial resolution of images. Used in\n" +
        "            combination with \\centers\\ and \n" +
        "            \\image_size\\ to generate images. Spatial\n" +
        "            resolution defines how many metres a pixel\n" +
        "            represents.")
    sub_parser.add_argument(
        '--save-to', type=str,
        default='data/',
        dest='save_to',
        help="Default: 'data-download/'. Directory to save images to.")
    # logging.info(
    #     f"Data Shell: Log level set to \"{logging.getLogger()}\"")
    # logging.info(
    #     f"Data Shell: Instance ID file used \"{args.instance_id}\"")
    # logging.info(
    #     f"Data Shell: Shopping List file used \"{args.shopping_list}\"")
