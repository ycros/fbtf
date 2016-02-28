from exceptions import FoobarException
from foobar import Foobar
from tests.base import FoobarTest


class FnCallTest(FoobarTest):

    def test_string_arg(self):
        f = Foobar()
        self.assertEqual("$len('meep')", f.len("meep").output())

    def test_blank(self):
        f = Foobar()
        self.assertEqual("$len()", f.len().output())

    def test_multi_arg(self):
        f = Foobar()
        self.assertEqual("$moo('awesome',3,4)", f.moo('awesome', 3, 4).output())

    def test_nested(self):
        f = Foobar()
        self.assertEqual("$foo(2,$bar('blah'),7)", f.foo(2, f.bar('blah'), 7).output())

    def test_keyword_args(self):
        f = Foobar()
        with self.assertRaises(FoobarException):
            f.foo(bar=5)

    def test_leading_underscore(self):
        f = Foobar()
        self.assertEqual("$if('a','b','c')", f._if('a', 'b', 'c').output())

    def test_chaining(self):
        f = Foobar()
        self.assertEqual("$left(%path%,2)", f['path'].left(2).output())

    def test_chaining2(self):
        f = Foobar()
        self.assertEqual("$right($left(%path%,$len(%path%)),2)", f['path'].left(f['path'].len()).right(2).output())