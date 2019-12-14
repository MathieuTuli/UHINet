"""
UHINet Testing Module
"""
from argparse import ArgumentParser
from pathlib import Path

import logging
import signal
import sys

from ..file_manager import file_exists
from .....components import LogLevel

print("\n---------------------------------")
print("UHINet Testing Module")
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
                    choices=['landsat-RGB-LST'],
                    required=True,
                    help="Data source for download.")
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
logging.info(
    f"Testing Shell: Log level set to \"{logging.getLogger()}\"")
logging.info(
    f"Testing Shell: Instance ID file used \"{args.instance_id}\"")
logging.info(
    f"Testing Shell: Shopping List file used \"{args.shopping_list}\"")


def control_c_handler(_signal, frame):
    print("\n---------------------------------")
    print("Testing Shell: Ctrl-C. Shutting Down.")
    print("---------------------------------")
    sys.exit(0)


signal.signal(signal.SIGINT, control_c_handler)


def main():
    if args.data_source.lower() == 'landsat-RGB-LST':
        logging.warning(
            "Testing Shell: Currently, only landsat RGB LST testing" +
            " are permitted")
        path = Path(args.shopping_list)
        if file_exists(path):
            logging.info("Testing Shell: Using shopping list" +
                         f"list found at \"{args.shopping_list}\"")

            with Path(args.instance_id).open() as f:
                instance_id = f.read().strip()

    else:
        logging.error(
            f"Testing Shell: Data source \"{args.data_source.lower()}\" " +
            "unknown.")
        sys.exit(0)
