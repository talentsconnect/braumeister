#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys

from colorama import Fore

from braumeister.settings import Settings


class Git:

    @staticmethod
    def check_working_directory():
        pipe = subprocess.PIPE
        process = subprocess.Popen(['git', 'status'], stdout=pipe, stderr=pipe)
        _, stderroutput = process.communicate()

        if not process.returncode == 0:
            if Settings.get("general", "verbose", False):
                print(stderroutput.decode("utf-8"))

            print(Fore.RED + "[-] " + Fore.RESET + "Please call the script from within your git directory")
            if (not Settings.is_dry_run()):
                sys.exit(1)

    @staticmethod
    def check_git_state():
        pipe = subprocess.PIPE
        process = subprocess.Popen(['git', 'status', "-s"], stdout=pipe, stderr=pipe)
        stdoutput, _ = process.communicate()

        if len(stdoutput.splitlines()) != 0:
            if Settings.get("general", "verbose", False):
                print(stdoutput.decode("utf-8"))

            print(Fore.RED + "[-] " + Fore.RESET + "There are uncommited changes in your current branch.")
            print(Fore.RED + "[-] " + Fore.RESET + "Please commit and call the script again!")
            if (not Settings.is_dry_run()):
                sys.exit(1)

    @staticmethod
    def create_candidate_branch(fix_version):
        current = Git.find_candidate_branch_name(fix_version)

        next_rc = 1
        if current:
            next_rc = int(current[-3:]) + 1

        new_branch_name = "release/" + fix_version.replace(" ", "_") + "_RC_" + format(next_rc, '03d')

        Git.create_new_branch_from_master(new_branch_name)
        return new_branch_name

    @staticmethod
    def create_release_branch(fix_version):
        new_branch_name = Git.find_release_branch_name(fix_version)

        Git.create_new_branch_from_master(new_branch_name)
        return new_branch_name

    @staticmethod
    def create_new_branch_from_master(new_branch_name):
        print(Fore.GREEN + "[+] " + Fore.RESET + "Creating new branch '" + Fore.GREEN + new_branch_name + Fore.RESET + "' from master")

        if (not Settings.is_dry_run()):
            print(Fore.BLUE)
            subprocess.call(["git", "checkout", "-b", new_branch_name, "origin/master"])
            print(Fore.RESET)

    @staticmethod
    def find_candidate_branch_name(fix_version):
        Git.call_git_command(["git", "fetch"])

        pipe = subprocess.PIPE

        try:
            process = subprocess.Popen(['git', 'branch', '-a', '--no-color'], stdout=pipe, stderr=pipe)
            output = subprocess.check_output(('grep', fix_version.replace(" ", "_")), stdin=process.stdout, stderr=process.stdout)

            process.communicate()
        except Exception as e:
            return ""

        existing_branches = []
        for line in output.splitlines():
            existing_branches.append(line.decode("utf-8"))

        highest_existing_branch_name = Git.get_max_candidate_branch_name(existing_branches)
        if not highest_existing_branch_name:
            print(Fore.YELLOW + "[*] " + Fore.RESET + "There is no existing RC for release %s" % fix_version)
        else:
            print(Fore.GREEN + "[+] " + Fore.RESET + "The last branch for RC %s is: %s" % (fix_version, highest_existing_branch_name))

        return highest_existing_branch_name

    @staticmethod
    def find_release_branch_name(fix_version):
        return "release/" + fix_version.replace(" ", "_") + "_GA"

    @staticmethod
    def get_max_candidate_branch_name(existing_branches):
        max_rc = 0
        max_branch_name = ""

        if not existing_branches:
            return max_branch_name

        for branch in existing_branches:
            current = int(branch[-3:])
            if (current > max_rc):
                max_rc = current
                max_branch_name = branch

        return max_branch_name

    @staticmethod
    def get_current_branch():
        pipe = subprocess.PIPE
        process = subprocess.Popen(['git', 'status'], stdout=pipe, stderr=pipe)
        stdoutput, _ = process.communicate()

        stdoutput = stdoutput.decode("utf-8")

        first_line = stdoutput.splitlines()[0]
        branch_name = first_line.split()[2]
        return branch_name

    @staticmethod
    def merge_branches(branches, target_branch, resume_code):
        current_branch = ""
        code = resume_code
        for key in branches:
            current_branch = key
            try:
                if Settings.get("general", "verbose", False):
                    print("------------------------------------")

                print(Fore.GREEN + "[🍻 ] " + Fore.RESET +
                      "Merging %s into %s..." % (current_branch, target_branch))

                if code == 0:
                    code = 1
                    if (not Settings.is_dry_run()):
                        Git.call_git_command(["git", "checkout", current_branch])

                if code == 1:
                    code = 2
                    if (not Settings.is_dry_run()):
                        Git.call_git_command(["git", "pull"])

                if code == 2:
                    code = 3
                    if (not Settings.is_dry_run()):
                        Git.call_git_command(["git", "merge", "origin/master"])

                if code == 3:
                    code = 4
                    if (not Settings.is_dry_run()):
                        Git.call_git_command(["git", "push", "origin", current_branch])

                if code == 4:
                    code = 5
                    if (not Settings.is_dry_run()):
                        Git.call_git_command(["git", "checkout", target_branch])

                if code == 5:
                    code = 6
                    if (not Settings.is_dry_run()):
                        Git.call_git_command(["git", "merge", "origin/" + current_branch])

                if code == 6:
                    code = 0
                    if (not Settings.is_dry_run()):
                        Git.call_git_command(["git", "branch", "-D", current_branch])
                    print(Fore.GREEN + "[🍻 ] " + Fore.RESET + "Branch '" + Fore.GREEN + current_branch + Fore.RESET + "' merged")
                    print("")
            except ValueError as e:
                raise GitException(current_branch, code)

    @staticmethod
    def delete_branches(branches):
        current_branch = ""
        for key in branches:
            current_branch = key
            try:
                if Settings.get("general", "verbose", False):
                    print("------------------------------------")

                print(Fore.GREEN + "[🍻 ] " + Fore.RESET + "Deleting %s..." % current_branch)

                if (not Settings.is_dry_run()):
                    try:
                        Git.call_git_command(["git", "push", "origin",  ":" + current_branch])
                    except:
                        print(Fore.YELLOW + "[*] " + Fore.RESET + "Error ocurred while deleting remote branch %s, please verify deletion manually" % current_branch)
                    try:
                        Git.call_git_command(["git", "branch", "-D", current_branch])
                    except Exception as e:
                        print(Fore.YELLOW + "[*] " + Fore.RESET + "Error ocurred while deleting local branch %s, please verify deletion manually" % current_branch)

            except ValueError as e:
                raise GitException(current_branch, 0)

    @staticmethod
    def push_branch(branch_name):
        if (not Settings.is_dry_run()):
            Git.call_git_command(["git", "push", "-u", "origin", branch_name])

    @staticmethod
    def call_git_command(param):
        if Settings.get("general", "verbose", False):
            print(Fore.GREEN + "[+] " + Fore.RESET + "Calling: " + Fore.BLUE + " ".join(param) + Fore.RESET)

        pipe = subprocess.PIPE
        process = subprocess.Popen(param, stdout=pipe, stderr=pipe)
        stdoutput, _ = process.communicate()

        if Settings.get("general", "verbose", False):
            print(stdoutput.decode("utf-8"))

        if process.returncode != 0:
            raise ValueError('Error after calling git command')


class GitException(Exception):
    def __init__(self, abort_branch, resume_code):
        Exception.__init__(self, abort_branch, resume_code)
        self.abort_branch = abort_branch
        self.resume_code = resume_code
