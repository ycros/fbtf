from output import Optimizer
from tests.base import FoobarTest


class OptimizerTest(FoobarTest):

    def setUp(self):
        super().setUp()
        self.o = Optimizer()

    def test_optimize(self):
        f = self.f
        ast = f.foo(f.bar(1), f.bar(2), f.bar(1))
        self.assertEqual(f.foo(f.put(f.id('v0'), f.bar(1)), f.bar(2), f.get(f.id('v0'))), self.o.optimize(ast))

    def test_nested_optimize(self):
        f = self.f
        inner_child = f.moo(f.thing(), 7)
        child = f.bar(inner_child, 3, inner_child)
        ast = f.foo(child, child)

        expected = f.foo(
            f.put(f.id('v0'), f.bar(
                f.put(f.id('v1'), f.moo(f.thing(), 7)), 3, f.get(f.id('v1'))
            )),
            f.get(f.id('v0'))
        )

        self.assertEqual(expected, self.o.optimize(ast))

    def test_nested_optimize_with_inner_reuse(self):
        f = self.f
        inner_child = f.moo(f.thing(), 7)
        child = f.bar(inner_child, 3, inner_child)
        ast = f.foo(child, child, inner_child)

        expected = f.foo(
            f.put(f.id('v0'), f.bar(
                f.put(f.id('v1'), f.moo(f.thing(), 7)), 3, f.get(f.id('v1'))
            )),
            f.get(f.id('v0')),
            f.get(f.id('v1'))
        )

        self.assertEqual(expected, self.o.optimize(ast))
