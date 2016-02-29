import unittest

from fbtf.output import output
from fbtf import Foobar


class FoobarTest(unittest.TestCase):
    def setUp(self):
        self.f = Foobar()

    def assertNodeOutput(self, expected_output, node):
        self.assertEqual(expected_output, output(node))
