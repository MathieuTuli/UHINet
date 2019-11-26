"""
UHINet Data Module
"""
from argparse import ArgumentParser
from path import Path

import logging
import sys

# from .SentinelHubAccessor import SentinelHubAccessor
from .data.download_landsat import download_lansat_from_file
from .file_manager import file_exists
from ..components import LogLevel


parser = ArgumentParser(description=__doc__)
parser.add_argument(
    '-v', '--verbose', action='store_true',
    dest='verbose',
    description="Set verbosity. In effect, set --log-level to DEBUG.")
parser.set_defaults(verbose=False)
parser.add_argument('--log-level', type=LogLevel.__getitem__,
                    default=LogLevel.INFO,
                    choices=LogLevel.__members__.values(),
                    dest='log_level',
                    description="")
parser.add_argument('--data-source', type=str.lower,
                    dest='data_source',
                    choices=['landsat'],
                    description="")
parser.add_argument('--instance-id', type=str,
                    default='instance_id.txt',
                    dest='instance_id',
                    description="")
parser.add_argument('--shopping-list', type=str,
                    default='shopping_list.txt',
                    dest='shopping_list',
                    description="")

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
        f"Shell: Warning: Log level \"{args.log_level}\" unknown, defaulting" +
        " to INFO.")


def main():
    print("\nUHINet Data Module")
    if args.data_source.lower() == 'landsat':
        logging.warning(
            "Shell: Warning: Currently, only landsat downloads from a " +
            "shopping list file are permitted")
        if file_exists(args.shopping_list):
            logging.info("Shell: Message: Downloading landsat from shopping " +
                         "list found at \"{args.shopping_list}\"")
            download_lansat_from_file(Path(args.shopping_list))

    else:
        logging.error(
            f"Data source \"{args.data_source.lower()}\" unknown. Exiting.")
        sys.exit(0)
