from .nodes import FnCallNode, VarNode, MemoizeNode, to_node, IdentifierNode


class Foobar:
    def __init__(self):
        self._memoize_counter = 0

    @staticmethod
    def var(name):
        return VarNode(name)

    @staticmethod
    def val(item):
        return to_node(item)

    @staticmethod
    def id(item):
        return IdentifierNode(item)

    def memoize(self, item):
        self._memoize_counter += 1
        return MemoizeNode(item)

    def __getitem__(self, item):
        return self.var(item)

    def __getattr__(self, name):
        return FnCallNode(name)


