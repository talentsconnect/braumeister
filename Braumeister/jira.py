#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import requests
from colorama import Fore

from braumeister.settings import Settings

class Jira:

    @staticmethod
    def get_feature_branches(fix_version):
        json_object = Jira.get_relevant_issues(fix_version)
        branches = {}

        if not "issues" in json_object:
            return {}

        custom_field_name = Settings.get(
            "jira", "branch_custom_field_id", None)

        if not custom_field_name:
            raise ValueError(
                "Missing 'branch_custom_field_id' in 'jira' section. Please run 'braumeister init'")

        for issue in json_object["issues"]:
            obj = Jira.get_specific_issue(issue["self"])
            value = []
            issue = obj["key"]
            # e.g. customfield_11219

            if not custom_field_name in obj["fields"]:
                raise ValueError("Missing %s in jira custom fields. Are you sure the name is %s? I've found these: \n%s" % (
                    custom_field_name, custom_field_name, ", ".join(obj["fields"])))

            key = obj["fields"][custom_field_name]

            if not key:
                print(Fore.YELLOW + "[~] " + Fore.RESET + "Ticket with empty branch field found: %s - Ignoring." % issue)
                continue

            if key in branches:
                issues = branches[key]
                issues.append(issue)
                branches[key] = issues
            else:
                value.append(issue)
                branches[key] = value

        return branches

    @staticmethod
    def get_relevant_issues(fix_version):
        print(Fore.GREEN + "[*] " + Fore.RESET + "Requesting all issues with fixVersion: " + Fore.GREEN + fix_version + Fore.RESET)

        jira_url = Settings.get("jira", "url", None)

        if not jira_url:
            raise ValueError("Missing 'url' in 'jira' section. Please run 'braumeister init'")

        query = "fixVersion=\"" + fix_version + "\" ORDER BY updated DESC"
        data = {"jql": query}
        url = "%s/rest/api/2/search" % jira_url

        return Jira.call_jira_post(url, json.dumps(data))

    @staticmethod
    def update_jira_issues(issues):
        print("------------------------------------")
        print(Fore.GREEN + "[+]" + Fore.RESET + " Update status to Staging needed on all related jira issues!")

        jira_url = Settings.get("jira", "url", None)
        if not jira_url:
            raise ValueError("Missing 'url' in 'jira' section. Please run 'braumeister init'")

        jira_destination_transition = Settings.get("jira", "destination_transition", None)
        if not jira_destination_transition:
            raise ValueError("Missing 'destination_transition' in 'jira' section. Please run 'braumeister init'")

        for issue in issues:
            url = "%s/rest/api/2/issue/%s/transitions" % (jira_url, issue)
            print("------------------------------------")
            print("Requesting all transitions for: " + issue)
            obj = Jira.call_jira_get(url)
            for transition in obj["transitions"]:
                if "Staging Needed" in transition["name"]:
                    Jira.update_jira_issue(issue, transition, url)

    @staticmethod
    def update_jira_issue(issue, transition, url):
        data = {
            "transition": {
                "id": transition["id"]
            }
        }
        print("Updating jira status on " + issue + " to " + transition["name"])

        if (not Settings.is_dry_run()):
            Jira.call_jira_post(url, json.dumps(data))

    @staticmethod
    def get_specific_issue(url):
        print(Fore.GREEN + "[+] " + Fore.RESET + "Requesting issue: " + url)

        return Jira.call_jira_get(url)

    @staticmethod
    def call_jira_post(url, data):
        jira_user = Settings.get("jira", "username", None)
        jira_password = Settings.get("jira", "password", None)

        if not jira_user:
            raise ValueError(
                "Missing 'username' in 'jira' section. Please run 'braumeister init'")

        if not jira_password:
            raise ValueError(
                "Missing 'password' in 'jira' section. Please run 'braumeister init'")

        response = requests.post(url, data=data, auth=(jira_user, jira_password), headers={'content-type': 'application/json'})

        try:
            return json.loads(response.text)
        except ValueError as error:
            return None

    @staticmethod
    def call_jira_get(url):
        jira_user = Settings.get("jira", "username", None)
        jira_password = Settings.get("jira", "password", None)

        if not jira_user:
            raise ValueError("Missing 'username' in 'jira' section. Please run 'braumeister init'")

        if not jira_password:
            raise ValueError("Missing 'password' in 'jira' section. Please run 'braumeister init'")

        response = requests.get(url, auth=(jira_user, jira_password), headers={'content-type': 'application/json'})

        try:
            return json.loads(response.text)
        except ValueError as error:
            return None
