import os
import unittest
from unittest.loader import TestLoader


def load_tests(loader: TestLoader, standard_tests, pattern):
    # top level directory cached on loader instance
    this_dir = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir)
    standard_tests.addTests(package_tests)
    return standard_tests


if __name__ == '__main__':
    unittest.main()
