import unittest
from foobar import Foobar
from exceptions import FoobarException


class FnCallTest(unittest.TestCase):

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


class ValTest(unittest.TestCase):

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


class VarTest(unittest.TestCase):

    def test_var(self):
        self.assertEqual("%hoo%", Foobar().var('hoo').output())

    def test_short_syntax(self):
        self.assertEqual("%moo%", Foobar()['moo'].output())


class MemoizeTest(unittest.TestCase):

    def test_memoization(self):
        f = Foobar()
        memoized = f.memoize(f.expensive())
        self.assertEqual("$put(v1,$expensive())", memoized.output())
        self.assertEqual("$put(v1,$expensive())", memoized.output())
        self.assertEqual("$moo($put(v1,$expensive()), $get(v1))", f.moo(memoized, memoized).output())

    @unittest.skip
    def test_multiple_memoizations(self):
        # broken test
        f = Foobar()
        m1 = f.memoize(f.one())
        m2 = f.memoize(f.two())
        self.assertEqual("$put(v1,$one())", m1.output())
        self.assertEqual("$put(v2,$two())", m2.output())
        self.assertEqual("$get(v1)", m1.output())
        self.assertEqual("$get(v2)", m2.output())


class MathsTest(unittest.TestCase):

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


class TestEquality(unittest.TestCase):

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

    def test_not_node(self):
        with self.assertRaises(FoobarException):
            Foobar.val(1) == 2


if __name__ == "__main__":
    unittest.main()
