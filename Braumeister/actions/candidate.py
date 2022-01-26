#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from colorama import Fore

from ..settings import Settings
from ..git import Git, GitException
from ..jira import Jira
from ..state import State


class Candidate:
    def __init__(self, fix_version, resume, update_jira):
        self.fix_version = fix_version
        self.resume = resume
        self.update_jira = update_jira

    def execute(self):
        Git.check_git_rerere()
        Git.check_working_directory()
        Git.check_git_state()

        if self.resume:
            data = State.read_file()
            branches = State.get_branches_from_data(data)
            candidate_branch_name = data["newBranchName"]
            resume_code = data["resumeCode"]
        else:
            branches = Jira.get_feature_branches(fix_version=self.fix_version)

            if not branches:
                print("")
                print(
                    Fore.RED
                    + "[-] "
                    + Fore.RESET
                    + "Found no issues for release candidate "
                    + Fore.GREEN
                    + "'"
                    + self.fix_version
                    + "'"
                    + Fore.RESET
                    + " in Jira."
                )
                print("    Please create a release in Jira first")
                print(
                    "      (and use the 'fixVersion' field to assign the release to a ticket) "
                )
                print("")
                sys.exit(1)

            candidate_branch_name = Git.create_candidate_branch(self.fix_version)
            resume_code = 0

        try:
            Git.merge_branches(branches, candidate_branch_name, resume_code)
        except GitException as e:
            self.handle_error(
                branches, candidate_branch_name, e.abort_branch, e.resume_code
            )

        State.delete_file()

        if self.update_jira:
            issues = State.get_issues_from_branches(branches)
            Jira.update_jira_issues(issues)

        Git.push_branch(candidate_branch_name)

        print("")
        print(Fore.GREEN + "[🍻 ] " + Fore.RESET + "All done. Grab a 🍺")
        print("")

    def handle_error(self, branches, candidate_branch_name, abort_branch, resume_code):
        data = State.get_data_from_branches(
            branches, candidate_branch_name, abort_branch, resume_code
        )
        State.write_file(data)

        current_branch = Git.get_current_branch()
        self.print_after_error(current_branch)

        sys.exit(1)

    def print_after_error(self, current_branch):
        main_branch_name = Settings.get("git", "main_branch_name", "master")

        if "release" in current_branch:
            print(
                f"\nA merge error occurred while merging feature into {current_branch}"
            )
        else:
            print(
                f"\nA merge error occurred while merging {main_branch_name} into {current_branch}"
            )

        print("\nPlease do the following steps:")
        print("\t* Resolve the conflicts")
        print("\t* Commit the changes")
        print("\t* Call the script again with the option -r \n")
