"""
UHINet Data Module
"""
from argparse import _SubParsersAction, Namespace as APNamespace
from pathlib import Path

import logging
import signal
import sys

from .download_landsat import download_lansat_from_file
from .SentinelHubAccessor import SentinelHubAccessor
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
        path = Path(args.shopping_list)
        if file_exists(path):
            logging.info("Data Shell: Downloading landsat from shopping " +
                         f"list found at \"{args.shopping_list}\"")

            with Path(args.instance_id).open() as f:
                instance_id = f.read().strip()

            sentinelhub_accessor = SentinelHubAccessor(instance_id)
            download_lansat_from_file(
                sentinelhub_accessor, path, Path(args.save_to))

    else:
        logging.error(
            f"Data Shell: Data source \"{args.data_source.lower()}\" unknown.")
        sys.exit(0)


def args(parser: _SubParsersAction) -> None:
    parser.add_argument('--data-source', type=str.lower,
                        dest='data_source',
                        choices=['landsat'],
                        required=True,
                        help="Data source for download.")
    parser.add_argument(
        '--instance-id', type=str,
        default='instance_id.txt',
        dest='instance_id',
        help="File name of instance id for data-set-specific API Accessor")
    parser.add_argument(
        '--shopping-list', type=str,
        default='shopping_list.json',
        dest='shopping_list',
        help="File name of settings and API demands for data-set-specific" +
        " download. See \"shopping_list_example.txt\" for an example.")
    parser.add_argument(
        '--save-to', type=str,
        default='data/images',
        dest='save_to',
        help="Directory to save images to.")
    # logging.info(
    #     f"Data Shell: Log level set to \"{logging.getLogger()}\"")
    # logging.info(
    #     f"Data Shell: Instance ID file used \"{args.instance_id}\"")
    # logging.info(
    #     f"Data Shell: Shopping List file used \"{args.shopping_list}\"")
