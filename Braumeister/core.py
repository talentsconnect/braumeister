import argparse
import sys

from colorama import init, Fore

from .builder import Builder
from .settings import Settings
from .setup import Setup

__version__ = "0.4.1"

class Core:

    def __init(self):
        init()

    def bootstap(self):
        #version = pkg_resources.require("braumeister")[0].version

        parser = argparse.ArgumentParser(
            description='Create (or finish up) a release (candidate) branch based on the "fixVersion" '
                        'field in JIRA and your `main` branch. (v' + __version__ + ")")

        parser.add_argument(
            'action',
            choices=['init', 'nightly', 'candidate', 'release', 'finalize', 'cleanup']
        )

        parser.add_argument(
            '-n',
            '--name',
            help='Name or version of your release (candidate)',
            action='store',
            dest='fix_version'
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

        parser.add_argument(
            '-dry',
            '--dry_run',
            help='Do not actually do anything, just try to',
            action='store_true'
        )

        args = parser.parse_args()

        if args.action == "init":
            setup = Setup()
            setup.run()
            sys.exit(0)
        else:
            if not args.fix_version:
                print(Fore.RED + "[-] " + Fore.RESET + "Error: missing -n FIX_VERSION parameter")
                sys.exit(1)

        Settings.load()
        Settings.set_dry_run(args.dry_run)

        builder = Builder(action=args.action,
                          fix_version=args.fix_version,
                          resume=args.resume,
                          update_jira=args.update_jira)

        try:
            builder.execute()
        except ValueError as error:
            print(Fore.RED + "[-] " + Fore.RESET + "Error: " + error.args[0])
        except AttributeError as error:
            print(Fore.RED + "[-] " + Fore.RESET + "Error: operation '" + args.action + "' not supported")
            print(f"Error: {error}")
        except Exception as error:
            print(Fore.RED + "[-] " + Fore.RESET + "Error: " + str(error))
