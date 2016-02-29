from fbtf.exceptions import FoobarException
from fbtf import Foobar
from tests.base import FoobarTest


class ValTest(FoobarTest):

    def test_int(self):
        self.assertNodeOutput("3", Foobar().val(3))

    def test_float(self):
        self.assertNodeOutput("3.14159", Foobar().val(3.14159))

    def test_function(self):
        f = Foobar()
        self.assertNodeOutput("$blah()", f.val(f.blah()))

    def test_var(self):
        f = Foobar()
        self.assertNodeOutput("%meep%", f.val(f.var('meep')))

    def test_invalid(self):
        with self.assertRaises(FoobarException):
            Foobar().val({})
