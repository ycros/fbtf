from exceptions import FoobarException
from foobar import Foobar
from tests.base import FoobarTest


class FnCallTest(FoobarTest):

    def test_string_arg(self):
        f = Foobar()
        self.assertNodeOutput("$len('meep')", f.len("meep"))

    def test_blank(self):
        f = Foobar()
        self.assertNodeOutput("$len()", f.len())

    def test_multi_arg(self):
        f = Foobar()
        self.assertNodeOutput("$moo('awesome',3,4)", f.moo('awesome', 3, 4))

    def test_nested(self):
        f = Foobar()
        self.assertNodeOutput("$foo(2,$bar('blah'),7)", f.foo(2, f.bar('blah'), 7))

    def test_keyword_args(self):
        f = Foobar()
        with self.assertRaises(FoobarException):
            f.foo(bar=5)

    def test_trailing_underscore(self):
        f = Foobar()
        self.assertNodeOutput("$if('a','b','c')", f.if_('a', 'b', 'c'))

    def test_chaining(self):
        f = Foobar()
        self.assertNodeOutput("$left(%path%,2)", f['path'].left(2))

    def test_chaining2(self):
        f = Foobar()
        self.assertNodeOutput("$right($left(%path%,$len(%path%)),2)", f['path'].left(f['path'].len()).right(2))
