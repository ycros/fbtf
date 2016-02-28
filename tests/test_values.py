from exceptions import FoobarException
from foobar import Foobar
from tests.base import FoobarTest


class ValTest(FoobarTest):

    def test_int(self):
        self.assertEqual("3", Foobar().val(3).output())

    def test_float(self):
        self.assertEqual("3.14159", Foobar().val(3.14159).output())

    def test_function(self):
        f = Foobar()
        self.assertEqual("$blah()", f.val(f.blah()).output())

    def test_var(self):
        f = Foobar()
        self.assertEqual("%meep%", f.val(f.var('meep')).output())

    def test_invalid(self):
        with self.assertRaises(FoobarException):
            Foobar().val({})
