#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import os.path

from braumeister.settings import Settings

class State:

    @staticmethod
    def write_file(state):
        print("\nWriting state json!")
        if (not Settings.is_dry_run()):
            with open('release_state.json', 'w') as outfile:
                json.dump(state, outfile, indent=4)

    @staticmethod
    def read_file():
        print("Reading state json!")
        with open('release_state.json') as json_file:
            return json.load(json_file)

    @staticmethod
    def delete_file():
        if os.path.isfile("release_state.json"):
            print("Deleting state json!")
            if (not Settings.is_dry_run()):
                os.remove("release_state.json")

    @staticmethod
    def get_data_from_branches(branches, release_branch_name, abort_branch, resume_code):
        data = {}
        data['branches'] = []
        data['newBranchName'] = release_branch_name
        data['resumeCode'] = resume_code

        for key in branches:
            data['branches'].append({
                'name': key,
                'abort': key == abort_branch,
                'issues': branches[key]
            })

        return data

    @staticmethod
    def get_branches_from_data(data):
        branches = {}
        found_abort = False

        for b in data['branches']:
            if b["abort"]:
                found_abort = True
                print("Resuming with " + b["name"])
            if found_abort:
                branches[b["name"]] = b["issues"]

        return branches

    @staticmethod
    def get_issues_from_branches(branches):
        issues = []

        for key in branches:
            issues += branches[key]

        print(issues)
        return issues
