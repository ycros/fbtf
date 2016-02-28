import unittest

from foobar import Foobar
from output import output


class FoobarTest(unittest.TestCase):
    def setUp(self):
        self.f = Foobar()

    def assertNodeOutput(self, expected_output, node):
        self.assertEqual(expected_output, output(node))