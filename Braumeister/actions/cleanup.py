#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from colorama import Fore

from braumeister.git import Git, GitException
from braumeister.jira import Jira


class Cleanup:

    def __init__(self, fix_version, resume, update_jira):
        self.fix_version = fix_version
        self.resume = resume
        self.update_jira = update_jira

    def execute(self):
        Git.check_working_directory()
        Git.check_git_state()

        branches = Jira.get_feature_branches(fix_version=self.fix_version)

        if not branches:
            print("")
            print(Fore.RED + "[-] " + Fore.RESET + "Found no issues for release " + Fore.GREEN + "'" + self.fix_version + "'" + Fore.RESET + " in Jira.")
            print("")
            sys.exit(1)

        try:
            Git.delete_branches(branches)
        except GitException as e:
            self.handle_error()

        print("")
        print(Fore.GREEN + "[🍻 ] " + Fore.RESET + "Brewhouse all clean again. Grab a 🍺")
        print("")

    def handle_error(self):
        current_branch = Git.get_current_branch()
        self.print_after_error(current_branch)

        sys.exit(1)

    def print_after_error(self, current_branch):
        print("\nFailed to delete local/remote branch " + current_branch)
        print("\nPlease do the following steps:")
        print("\t* Resolve the errors")
        print("\t* Commit the changes")
        print("\t* Call the script again\n")
