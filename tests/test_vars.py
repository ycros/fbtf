from fbtf import Foobar
from tests.base import FoobarTest


class VarTest(FoobarTest):

    def test_var(self):
        self.assertNodeOutput("%hoo%", Foobar().var('hoo'))

    def test_short_syntax(self):
        self.assertNodeOutput("%moo%", Foobar()['moo'])
