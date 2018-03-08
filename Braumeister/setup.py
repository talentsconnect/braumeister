#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import getpass
from colorama import Fore
from braumeister.settings import Settings

HEADER = "\
  ,---.   ,---.    .--.  .-. .-.         ,---." + Fore.WHITE + ",-. " + Fore.GREEN + "  .---.  _______ ,---.  ,---.    \n\
 | .-.\  | .-.\  / /\ \ | | | ||\    /| | .-'  " + Fore.WHITE + "|(| " + Fore.GREEN + " ( .-._)|__   __|| .-'  | .-.\    \n\
 | |-' \ | `-'/ / /__\ \| | | ||(\  / | | `-.  " + Fore.WHITE + "(~) " + Fore.GREEN + " (_) \     )| |   | `-.  | `-'/    \n\
 | |--. \|   (  |  __  || | | |(_)\/  | | .-'  " + Fore.YELLOW + "|o|" + Fore.GREEN + " _  \ \   (_) |   | .-'  |   (     \n\
 | |`-' /| |\ \ | |  |)|| `-')|| \  / | |  `--." + Fore.YELLOW + "|O|" + Fore.GREEN + "( `-'  )    | |   |  `--.| |\ \    \n\
 /( `--' |_| \)\|_|  (_)`---(_)| |\/| | /( __.'" + Fore.YELLOW + "`-'" + Fore.GREEN + " `----'     `-'   /( __.'|_| \)\   \n\
(__)         (__)              '-'  '-'(__)                        (__)        (__)  \n\
"


def default_validator(_):
    """ Returns true, every time. """
    return True


class Setup:
    """ Setup Wizard """

    def __init__(self):
        self.jira_url = ""
        self.jira_user = ""
        self.jira_pass = ""
        self.jira_destination_transition = ""
        self.jira_branch_field_id = ""

    def print_success(self, message):
        print("%s[*]%s %s" % (Fore.GREEN, Fore.RESET, message))

    def print_error(self, message):
        print("%s[!] %s %s" % (Fore.RED, Fore.RESET, message))

    def print_question(self, question):
        return input(Fore.GREEN + "[?] " + Fore.RESET + question + ": ")

    def ask_required(self, question, error_message="Please anwer the question", secure=False, validator=default_validator):
        answer = ""

        while not answer or not validator(answer):
            if secure:
                answer = getpass.getpass(
                    Fore.GREEN + "[?] " + Fore.RESET + question + ": "
                )
            else:
                answer = self.print_question(question)

            if not answer or not validator(answer):
                self.print_error(error_message)
                print()

        return answer

    def ask_optional(self, question):
        return self.print_question("%s (optional)" % question)

    def url_validator(self, url):
        """ checks if the given url starts with 'http' """
        return url.startswith("http")

    def ask_jira(self):
        """ Asking questions about the jira configuration """
        print()
        self.print_success("JIRA Configuration")
        self.print_success("----------------------")
        print()

        self.jira_url = self.ask_required(
            "URL", "Please enter a url that starts with http(s)://",
            False,
            self.url_validator
        )

        self.jira_user = self.ask_required(
            "Username",
            "Please enter a username"
        )

        self.jira_pass = self.ask_required(
            "Password",
            "Please enter a password",
            True
        )

        self.jira_branch_field_id = self.ask_required(
            "Custom Field Id for 'Branch'",
            "Please enter a custom field id"
        )

        self.jira_destination_transition = self.ask_optional(
            "Destination Transiton Name"
        )

    def run(self):
        """ Clearing the screen and asking the questions """
        os.system("clear")
        os.system("clear")

        print()
        print("%s %s %s" % (Fore.GREEN, HEADER, Fore.RESET))
        print()

        print("\t Please answer the following questions:")
        print()

        self.ask_jira()

        print()

        Settings.save("jira", "url", self.jira_url)
        Settings.save("jira", "username", self.jira_user)
        Settings.save("jira", "password", self.jira_pass)
        Settings.save("jira", "destination_transition",
                      self.jira_destination_transition)
        Settings.save("jira", "branch_custom_field_id",
                      self.jira_branch_field_id)

        print()
        self.print_success("Thank you.")
        self.print_success("We saved the config to %s" %
                           Settings.find_config_file())

        print()
