#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os.path
from pathlib import Path
from colorama import Fore

dry_run = False

class Settings:

    @staticmethod
    def set_dry_run(dry_run_state):
        global dry_run
        dry_run = dry_run_state

    @staticmethod
    def is_dry_run():
        global dry_run
        return dry_run

    @staticmethod
    def load():
        config = configparser.ConfigParser()
        config_file = Settings.find_config_file()
        if config_file is not None:
            config.read(config_file)
        else:
            Settings.write_default_conf(config)

        return config

    @staticmethod
    def write_default_conf(config):
        print(Fore.GREEN + "[+] " + Fore.RESET + "Writing my default config")

        config.add_section("general")
        config.set("general", "verbose", "false")

        Settings.save_config_file(config)

    @staticmethod
    def save_config_file(config):
        with open(Settings.get_config_file_name(), 'w') as config_file:
            config.write(config_file)

    @staticmethod
    def get_config_file_name():
        return ".braumeister"

    @staticmethod
    def find_config_file():
        config_file_name = Settings.get_config_file_name()
        current_working_dir = os.getcwd() + "/" + config_file_name
        home_dir = str(Path.home()) + "/" + config_file_name

        if os.path.isfile(current_working_dir):
            return current_working_dir
        elif os.path.isfile(home_dir):
            return home_dir

        return None

    @staticmethod
    def save(section, key, val):
        config = Settings.load()

        if not section in config.sections():
            config.add_section(section)

        config.set(section, key, str(val))
        Settings.save_config_file(config)

    @staticmethod
    def get(section, key, default_value=None):
        config = Settings.load()

        if not section in config.sections():
            return default_value

        if section == "general" and key == "verbose":
            return config["general"].getboolean("verbose")

        return config[section].get(key, default_value)
