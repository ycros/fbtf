from exceptions import FoobarException
from foobar import Foobar
from tests.base import FoobarTest


class TestEquality(FoobarTest):

    def test_fn(self):
        self.assertEqual(Foobar().foo(), Foobar().foo())
        self.assertNotEqual(Foobar().foo(), Foobar().bar())

    def test_fn_args(self):
        self.assertEqual(Foobar().foo(1, 2, 'a'), Foobar().foo(1, 2, 'a'))
        self.assertNotEqual(Foobar().foo(1, 2), Foobar().foo(2, 1))

    def test_val_num(self):
        self.assertEqual(Foobar.val(1), Foobar.val(1))
        self.assertNotEqual(Foobar.val(1), Foobar.val(2))

    def test_val_float(self):
        self.assertEqual(Foobar.val(1.1), Foobar.val(1.1))
        self.assertNotEqual(Foobar.val(1.1), Foobar.val(2.2))

    def test_val_string(self):
        self.assertEqual(Foobar.val('hi'), Foobar.val('hi'))
        self.assertNotEqual(Foobar.val('hi'), Foobar.val('ho'))

    def test_var(self):
        self.assertEqual(Foobar.var('hi'), Foobar.var('hi'))
        self.assertNotEqual(Foobar.var('hi'), Foobar.var('ho'))

    def test_memoize(self):
        f = Foobar()
        self.assertEqual(f.memoize(f.foo()), f.memoize(f.foo()))
        self.assertNotEqual(f.memoize(f.foo()), f.memoize(f.bar()))

    def test_id(self):
        f = Foobar()
        self.assertEqual(Foobar.id('hi'), Foobar.id('hi'))
        self.assertNotEqual(Foobar.id('hi'), Foobar.id('ho'))

    def test_not_node(self):
        with self.assertRaises(FoobarException):
            Foobar.val(1) == 2