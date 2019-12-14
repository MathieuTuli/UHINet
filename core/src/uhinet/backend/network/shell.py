"""
UHINet Pix2Pix Module
"""
from argparse import ArgumentParser

import logging
import signal
import sys

from ...components import LogLevel

print("\n---------------------------------")
print("UHINet Pix2Pix Module")
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
    f"Data Shell: Log level set to \"{logging.getLogger()}\"")


def control_c_handler(_signal, frame):
    print("\n---------------------------------")
    print("Data Pix2Pix: Ctrl-C. Shutting Down.")
    print("---------------------------------")
    sys.exit(0)


signal.signal(signal.SIGINT, control_c_handler)


def main():
    ...
