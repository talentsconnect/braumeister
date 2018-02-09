from unittest import TestCase, main
from ..settings import Settings

class SettingsTest(TestCase):

    def test_test(self):
        self.assertEqual("hund", "hund")

    def test_has_config_file(self):
        f = Settings.find_config_file()
        print("file: %s" % f)
        
        self.assertIsNotNone(f)

if __name__ == '__main__':
    main()