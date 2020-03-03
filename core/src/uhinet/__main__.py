from argparse import ArgumentParser, RawTextHelpFormatter
import logging
import matplotlib

from .components import LogLevel
from .backend.data.shell import main as data_main, args as data_args
from .frontend.run import main as frontend_main, args as frontend_args

matplotlib.use('Agg')


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
subparser = parser.add_subparsers(dest='command')
data_subparser = subparser.add_parser(
    'download-data', help='Data commands',
    formatter_class=RawTextHelpFormatter)
data_args(data_subparser)
frontend_subparser = subparser.add_parser(
    'frontend', help='Frontend commands')
frontend_args(frontend_subparser)

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
    args.log_level = 'INFO'
    logging.warning(
        f"Frontend: Log level \"{args.log_level}\" unknown, defaulting" +
        " to INFO.")
logging.info(f"UHINET: Log Level set to {str(args.log_level)}")

if __name__ == "__main__":
    if str(args.command) == 'download-data':
        data_main(args)
    elif str(args.command) == 'frontend':
        frontend_main(args)
    else:
        logging.critical(f"UHINET: Unknown subcommand {args.command}")
