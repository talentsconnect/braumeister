#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from colorama import Fore

from braumeister.git import Git, GitException
from braumeister.jira import Jira
from braumeister.state import State


class Release:

    def __init__(self, fix_version, resume, update_jira):
        self.fix_version = fix_version
        self.resume = resume
        self.update_jira = update_jira

    def execute(self):
        Git.check_working_directory()
        Git.check_git_state()

        if self.resume:
            data = State.read_file()
            branches = State.get_branches_from_data(data)
            release_branch_name = data['newBranchName']
            resume_code = data['resumeCode']
        else:
            branches = Jira.get_feature_branches(fix_version=self.fix_version)

            if not branches:
                print("")
                print(Fore.RED + "[-] " + Fore.RESET + "Found no issues for release " + Fore.GREEN + "'" + self.fix_version + "'" + Fore.RESET + " in Jira.")
                print("    Please create a release in Jira first")
                print("      (and use the 'fixVersion' field to assign the release to a ticket) ")
                print("")
                sys.exit(1)

            release_branch_name = Git.create_release_branch(
                self.fix_version)
            resume_code = 0

        try:
            Git.merge_branches(branches, release_branch_name, resume_code)
        except GitException as e:
            self.handle_error(branches,
                              release_branch_name,
                              e.abort_branch,
                              e.resume_code)

        State.delete_file()

        if self.update_jira:
            issues = State.get_issues_from_branches(branches)
            Jira.update_jira_issues(issues)

        Git.push_branch(release_branch_name)

        print("")
        print(Fore.GREEN + "[🍻 ] " + Fore.RESET + "All done. Grab a 🍺")
        print("")

    def handle_error(self, branches, release_branch_name, abort_branch, resume_code):
        data = State.get_data_from_branches(
            branches, release_branch_name, abort_branch, resume_code)
        State.write_file(data)

        current_branch = Git.get_current_branch()
        self.print_after_error(current_branch)

        sys.exit(1)

    def print_after_error(self, current_branch):
        if "release" in current_branch:
            print("\nA merge error occurred while merging feature into " + current_branch)
        else:
            print("\nA merge error occurred while merging master into " + current_branch)

        print("\nPlease do the following steps:")
        print("\t* Resolve the conflicts")
        print("\t* Commit the changes")
        print("\t* Call the script again with the option -r \n")
