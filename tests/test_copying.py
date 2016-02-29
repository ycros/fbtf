from copy import copy

from nodes import FnCallNode, StrNode, NumberNode, VarNode, IdentifierNode, MemoizeNode
from tests.base import FoobarTest


class CopyTest(FoobarTest):
    def test_fn_call(self):
        n = FnCallNode('foo', StrNode('bar'))
        self.assertEqual(n, copy(n))

    def test_str(self):
        n = StrNode('foo')
        self.assertEqual(n, copy(n))

    def test_num(self):
        n = NumberNode(5)
        self.assertEqual(n, copy(n))

    def test_var(self):
        n = VarNode('foo')
        self.assertEqual(n, copy(n))

    def test_id(self):
        n = IdentifierNode('foo')
        self.assertEqual(n, copy(n))

    def test_memoize(self):
        n = MemoizeNode(FnCallNode('foo'))
        self.assertEqual(n, copy(n))
