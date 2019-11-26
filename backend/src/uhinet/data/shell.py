"""
UHINet Data Module
"""
print("\n---------------------------------")
print("UHINet Data Module")
print("---------------------------------\n")
from argparse import ArgumentParser
from pathlib import Path

import logging
import sys

# from .SentinelHubAccessor import SentinelHubAccessor
from .download_landsat import download_lansat_from_file
from ..file_manager import file_exists
from ..components import LogLevel


parser = ArgumentParser(description=__doc__)
parser.add_argument(
    '-v', '--verbose', action='store_true',
    dest='verbose',
    help="Set verbosity. In effect, set --log-level to DEBUG.")
parser.set_defaults(verbose=False)
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
    default='shopping_list.txt',
    dest='shopping_list',
    help="File name of settings and API demands for data-set-specific" +
    " download. See \"shopping_list_example.txt\" for an example.")

args = parser.parse_args()
if args.log_level == 'DEBUG' or args.verbose:
    logging.root.setLevel(logging.DEBUG)
elif args.log_level == 'INFO':
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
        f"Shell: Log level \"{args.log_level}\" unknown, defaulting" +
        " to INFO.")
logging.info(
    f"Shell: Log level set to \"{logging.getLogger()}\"")
logging.info(
    f"Shell: Instance ID file used \"{args.instance_id}\"")
logging.info(
    f"Shell: Shopping List file used \"{args.shopping_list}\"")


def main():
    if args.data_source.lower() == 'landsat':
        logging.warning(
            "Shell: Currently, only landsat downloads from a " +
            "shopping list file are permitted")
        path = Path(args.shopping_list)
        if file_exists(path):
            logging.info("Shell: Downloading landsat from shopping " +
                         "list found at \"{args.shopping_list}\"")
            download_lansat_from_file(path)

    else:
        logging.error(
            f"Shell: Data source \"{args.data_source.lower()}\" unknown.")
        sys.exit(0)
