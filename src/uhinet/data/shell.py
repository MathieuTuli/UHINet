"""
UHINet Data Module
"""
from argparse import ArgumentParser

import logging
import sys

# from .SentinelHubAccessor import SentinelHubAccessor


parser = ArgumentParser(description=__doc__)
parser.add_argument('-v', action='store_true',
                    dest='verbose')
parser.set_defaults(verbose=False)
parser.add_argument('--log-level', type=str, default='INFO',
                    dest='log_level')
parser.add_argument('--data-source', type=str,
                    default='', dest='data_source')

args = parser.parse_args()
if args.log_level == 'NOTSET':
    logging.root.setLevel(logging.INFO)
elif args.log_level == 'DEBUG' or args.verbose:
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
        f"Log level \"{args.log_level}\" unknown, defaulting to INFO.")
    logging.info(
        "FYI, allowed log levels include NOTSET, DEBUG, INFO, WARNING, " +
        "ERROR, CRITICAL.")


def main():
    print("\nUHINet Data Module")
    if args.data_source.lower() == 'landsat':
        # TODO FIgure out proper way to use instance id
        ...
    else:
        logging.error(
            f"Data source \"{args.data_source}\" unknown. Exiting.")
        sys.exit(0)
