"""
UHINet Data Module
"""
from argparse import ArgumentParser
from pathlib import Path

import sys
import logging

from .download_landsat import download_lansat_from_file
from .SentinelHubAccessor import SentinelHubAccessor
from ..file_manager import file_exists
from ..components import LogLevel

print("\n---------------------------------")
print("UHINet Data Module")
print("---------------------------------\n")

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

args = parser.parse_args()
if args.log_level == 'DEBUG' or args.very_verbose:
    logging.root.setLevel(logging.DEBUG)
elif args.log_level == 'INFO' or args.verbose:
    logging.root.setLevel(logging.INFO)
elif args.log_level == 'WARNING':
    logging.root.setLevel(logging.WARNING)
elif args.log_level == 'ERROR':
    logging.root.setLevel(logging.ERROR)
elif args.log_level == 'CRITICAL':
    logging.root.setLevel(logging.CRITICAL)
else:
    logging.root.setLevel(logging.INFO)
    logging.warning(
        f"Data Shell: Log level \"{args.log_level}\" unknown, defaulting" +
        " to INFO.")
logging.info(
    f"Data Shell: Log level set to \"{logging.getLogger()}\"")
logging.info(
    f"Data Shell: Instance ID file used \"{args.instance_id}\"")
logging.info(
    f"Data Shell: Shopping List file used \"{args.shopping_list}\"")


def main():
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
