import unittest

from foobar import Foobar
from tests.base import FoobarTest


class MemoizeTest(FoobarTest):
    def test_memoization(self):
        f = Foobar()
        memoized = f.memoize(f.expensive())
        self.assertNodeOutput("$put(v0,$expensive())", memoized)
        self.assertNodeOutput("$put(v0,$expensive())", memoized)
        self.assertNodeOutput("$moo($put(v0,$expensive()),$get(v0))", f.moo(memoized, memoized))

    def test_multiple_memoizations(self):
        # broken test
        f = Foobar()
        m1 = f.memoize(f.one())
        m2 = f.memoize(f.two())
        self.assertNodeOutput("$put(v0,$one())", m1)
        self.assertNodeOutput("$put(v0,$two())", m2)
        self.assertNodeOutput("$put(v0,$one())", m1)
        self.assertNodeOutput("$put(v0,$two())", m2)
        self.assertNodeOutput("$foo($put(v0,$one()),$bar($get(v0),$put(v1,$two())),$get(v1))",
                              f.foo(m1, f.bar(m1, m2), m2))
