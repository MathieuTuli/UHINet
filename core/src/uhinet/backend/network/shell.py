"""
UHINet Pix2Pix Module
"""
from argparse import _SubParsersAction, Namespace as APNamespace

import logging
import signal
import sys


def control_c_handler(_signal, frame):
    print("\n---------------------------------")
    print("Data Pix2Pix: Ctrl-C. Shutting Down.")
    print("---------------------------------")
    sys.exit(0)


def main(ags: APNamespace):
    print("\n---------------------------------")
    print("UHINet Pix2Pix Module")
    print("---------------------------------\n")
    signal.signal(signal.SIGINT, control_c_handler)


def args(parser: _SubParsersAction) -> None:
    ...
