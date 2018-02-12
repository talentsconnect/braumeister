#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, main
from ..settings import Settings


class SettingsTest(TestCase):

    def test_test(self):
        self.assertEqual("hund", "hund")

    def test_create_config_file(self):
        Settings.load()
        config_file = Settings.find_config_file()

        self.assertIsNotNone(config_file)

    def test_set_string(self):
        Settings.load()
        Settings.save("general", "hund", "wuff")
        val = Settings.get("general", "hund")
        
        self.assertEqual(val, "wuff")
    
    def test_get_bool(self):
        Settings.load()
        verbose = Settings.get("general", "verbose")

        self.assertEqual(verbose, False)


if __name__ == '__main__':
    main()
