import unittest

from foobar import Foobar
from tests.base import FoobarTest


class MemoizeTest(FoobarTest):

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