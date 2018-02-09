#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import pkg_resources
from colorama import init, Fore
from .builder import Builder
from .settings import Settings
from .setup import Setup

init()


def main():
    version = pkg_resources.require("Braumeister")[0].version

    parser = argparse.ArgumentParser(
        description='Create a release branch based on the "fixVersion" field in JIRA and your `master` branch. (v' + version + ")")
    
    parser.add_argument(
        'fix_version',
        help='e.g. "Krazy Kant"'
    )
    parser.add_argument(
        '-r',
        '--resume',
        help='Continue after last merge conflict',
        action='store_true'
    )
    parser.add_argument(
        '-u',
        '--update_jira',
        help='Also update Jira status after merging an issue',
        action='store_true'
    )
    args = parser.parse_args()

    if args.fix_version == "init":
        setup = Setup()
        setup.run()

        sys.exit(0)

    Settings.load()

    builder = Builder(fix_version=args.fix_version,
                      resume=args.resume,
                      update_jira=args.update_jira)

    try:
        builder.execute()
    except ValueError as error:
        print(Fore.RED + "[-] " + Fore.RESET + "Eror: " + error.args[0])


if __name__ == 'main':
    main()
