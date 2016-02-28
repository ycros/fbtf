from foobar import Foobar
from tests.base import FoobarTest


class VarTest(FoobarTest):

    def test_var(self):
        self.assertEqual("%hoo%", Foobar().var('hoo').output())

    def test_short_syntax(self):
        self.assertEqual("%moo%", Foobar()['moo'].output())
