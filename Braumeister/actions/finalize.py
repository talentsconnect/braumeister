#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from colorama import Fore

from ..settings import Settings
from ..git import Git, GitException


class Finalize:
    def __init__(self, fix_version, resume, update_jira):
        self.fix_version = fix_version
        self.resume = resume
        self.update_jira = update_jira

    def execute(self):
        Git.check_working_directory()
        Git.check_git_state()

        main_branch_name = Settings.get("git", "main_branch_name", "master")
        branches = {}

        try:
            sourceBranch = Git.find_release_branch_name(self.fix_version)
            branches = {sourceBranch}
            Git.merge_branches(branches, main_branch_name, 0)
        except GitException as e:
            self.handle_error()

        Git.push_branch(main_branch_name)

        print("")
        print(Fore.GREEN + "[🍻 ] " + Fore.RESET + "All done. Grab a 🍺")
        print("")

    def handle_error(self):
        current_branch = Git.get_current_branch()
        self.print_after_error(current_branch)

        sys.exit(1)

    def print_after_error(self, current_branch):
        main_branch_name = Settings.get("git", "main_branch_name", "master")

        print(
            f"\nA merge error occurred while merging {current_branch} into {main_branch_name}"
        )
        print("\nPlease do the following steps:")
        print("\t* Resolve the conflicts")
        print("\t* Commit the changes")
        print("\t* Call the script again\n")
