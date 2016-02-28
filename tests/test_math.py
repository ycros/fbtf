from foobar import Foobar
from tests.base import FoobarTest


class MathTest(FoobarTest):

    def test_subtract(self):
        f = Foobar()
        self.assertEqual("$sub($one(),3)", (f.one() - 3).output())

    def test_add(self):
        f = Foobar()
        self.assertEqual("$add($one(),3)", (f.one() + 3).output())

    def test_div(self):
        f = Foobar()
        self.assertEqual("$div($one(),3)", (f.one() / 3).output())

    def test_mul(self):
        f = Foobar()
        self.assertEqual("$mul($one(),3)", (f.one() * 3).output())