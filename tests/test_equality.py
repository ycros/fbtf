from exceptions import FoobarException
from foobar import Foobar
from tests.base import FoobarTest


class TestEquality(FoobarTest):

    def assertEqualIncludingHash(self, first, second):
        self.assertEqual(first, second)
        self.assertEqual(hash(first), hash(second))

    def assertNotEqualIncludingHash(self, first, second):
        # let's just assume we shouldn't collide for this set of test data.
        self.assertNotEqual(first, second)
        self.assertNotEqual(hash(first), hash(second))

    def test_fn(self):
        self.assertEqualIncludingHash(Foobar().foo(), Foobar().foo())
        self.assertNotEqualIncludingHash(Foobar().foo(), Foobar().bar())

    def test_fn_args(self):
        self.assertEqualIncludingHash(Foobar().foo(1, 2, 'a'), Foobar().foo(1, 2, 'a'))
        self.assertNotEqualIncludingHash(Foobar().foo(1, 2), Foobar().foo(2, 1))

    def test_val_num(self):
        self.assertEqualIncludingHash(Foobar.val(1), Foobar.val(1))
        self.assertNotEqualIncludingHash(Foobar.val(1), Foobar.val(2))

    def test_val_float(self):
        self.assertEqualIncludingHash(Foobar.val(1.1), Foobar.val(1.1))
        self.assertNotEqualIncludingHash(Foobar.val(1.1), Foobar.val(2.2))

    def test_val_string(self):
        self.assertEqualIncludingHash(Foobar.val('hi'), Foobar.val('hi'))
        self.assertNotEqualIncludingHash(Foobar.val('hi'), Foobar.val('ho'))

    def test_var(self):
        self.assertEqualIncludingHash(Foobar.var('hi'), Foobar.var('hi'))
        self.assertNotEqualIncludingHash(Foobar.var('hi'), Foobar.var('ho'))

    def test_memoize(self):
        f = Foobar()
        self.assertEqualIncludingHash(f.memoize(f.foo()), f.memoize(f.foo()))
        self.assertNotEqualIncludingHash(f.memoize(f.foo()), f.memoize(f.bar()))

    def test_id(self):
        self.assertEqualIncludingHash(Foobar.id('hi'), Foobar.id('hi'))
        self.assertNotEqualIncludingHash(Foobar.id('hi'), Foobar.id('ho'))

    def test_not_node(self):
        with self.assertRaises(FoobarException):
            Foobar.val(1) == 2

    def test_same_node(self):
        v = Foobar.val('moo')
        self.assertEqualIncludingHash(v, v)

    def test_different_nodes(self):
        self.assertNotEqualIncludingHash(Foobar.val('a'), Foobar.var('a'))
