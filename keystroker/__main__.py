#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Entry point script for keystroker"""

import argparse

from keystroker.sendkeys import sendkeys


def main():
    """main argparse for sending keystrokes through console"""
    parser = argparse.ArgumentParser(
        prog="keystroker",
        description="Sends one or more keystrokes combinations to the active "
                    "window."
    )
    group = parser.add_argument_group(title="Keystroke source")
    group = group.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", type=str,
                       help="Path to file containing keystrokes to send")
    group.add_argument("-k", "--keys", type=str,
                       help="String containing keystrokes to send")

    group = parser.add_argument_group(title="Keystroke timings")
    group.add_argument("-d", "--delay", type=float, default=0.0,
                       help="Time in seconds before sending keystrokes "
                            "default: %(default)s")
    group.add_argument("-p", "--pause", type=float, default=0.0,
                       help="Time in seconds between each keystroke "
                            "default: %(default)s")
    args = parser.parse_args()

    if args.delay < 0:
        raise ValueError("`DELAY` must be >= 0.0")

    if args.pause < 0:
        raise ValueError("`PAUSE` must be >= 0.0")

    if args.file is not None:
        with open(args.file) as f:
            keys = f.read()
            sendkeys(keys, args.pause)
    elif args.keys is not None:
        sendkeys(args.keys, args.pause)


if __name__ == "__main__":
    main()
