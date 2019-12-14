from argparse import ArgumentParser
import logging

from .components import LogLevel
from .backend.shell import backend_main, backend_args
from .frontend.run import frontend_main, frontend_args


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
subparser = parser.add_subparsers(dest='command')
backend_subparser = subparser.add_parser('backend', help='Backend commands')
backend_args(backend_subparser)
frontend_subparser = subparser.add_parser('frontend', help='Frontend commands')
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
    logging.warning(
        f"Frontend: Log level \"{args.log_level}\" unknown, defaulting" +
        " to INFO.")

if __name__ == "__main__":
    if str(args.command) == 'backend':
        backend_main()
    elif str(args.command) == 'backend':
        frontend_main()
    else:
        logging.critical(f"UHINET: Unknown subcommand {args.command}")
