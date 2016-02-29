from foobar import Foobar
from tests.base import FoobarTest


class MathTest(FoobarTest):

    def test_subtract(self):
        f = Foobar()
        self.assertNodeOutput("$sub($one(),3)", f.one() - 3)

    def test_add(self):
        f = Foobar()
        self.assertNodeOutput("$add($one(),3)", f.one() + 3)

    def test_div(self):
        f = Foobar()
        self.assertNodeOutput("$div($one(),3)", f.one() / 3)

    def test_mul(self):
        f = Foobar()
        self.assertNodeOutput("$mul($one(),3)", f.one() * 3)
