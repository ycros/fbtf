from abc import ABCMeta, abstractmethod
from .exceptions import FoobarException


class Node(metaclass=ABCMeta):
    def __init__(self):
        self.children = []

    def __add__(self, other):
        return FnCallNode('add')(self, other)

    def __sub__(self, other):
        return FnCallNode('sub')(self, other)

    def __mul__(self, other):
        return FnCallNode('mul')(self, other)

    def __truediv__(self, other):
        return FnCallNode('div')(self, other)

    def __getattr__(self, item):
        if item.startswith('__'):
            raise AttributeError
        return FnCallNode(item, self)

    def _add_child(self, child_node):
        if not isinstance(child_node, Node):
            raise FoobarException('Attempted to add a non-node as a child.')
        self.children.append(child_node)

    @abstractmethod
    def __hash__(self):
        result = hash(self.__class__)
        for i, child in enumerate(self.children):
            result ^= i + hash(child)  # take child order into account
        return result

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Node):
            raise FoobarException('Comparing a node to a non-node is invalid.')
        if self.__class__ != other.__class__:
            return False
        if self.children != other.children:
            return False
        return self._eq(other)

    @abstractmethod
    def _eq(self, other):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class FnCallNode(Node):
    def __init__(self, name, *args):
        super().__init__()
        self.name = name
        [self._add_child(arg) for arg in args]

    def __call__(self, *args, **kwargs):
        if len(kwargs) > 0:
            raise FoobarException('Passed keyword arguments to function call, unsupported.')
        [self._add_child(to_node(arg)) for arg in args]
        return self

    def __hash__(self):
        return super().__hash__() ^ hash(self.name)

    def _eq(self, other):
        return other.name == self.name

    def __repr__(self):
        return "{0}({1})".format(self.name, ', '.join(repr(x) for x in self.children))


class StrNode(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __hash__(self):
        return super().__hash__() ^ hash(self.value)

    def _eq(self, other):
        return other.value == self.value

    def __repr__(self):
        return "'{0}'".format(self.__name__)


class NumberNode(Node):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def __hash__(self):
        return super().__hash__() ^ hash(self.num)

    def _eq(self, other):
        return other.num == self.num

    def __repr__(self):
        return "{0}".format(self.num)


class VarNode(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __hash__(self):
        return super().__hash__() ^ hash(self.name)

    def _eq(self, other):
        return other.name == self.name

    def __repr__(self):
        return "%{0}%".format(self.name)


class MemoizeNode(Node):
    def __init__(self, child_node):
        super().__init__()
        self.child_node = child_node
        self._add_child(child_node)

    def __hash__(self):
        return super().__hash__()

    def _eq(self, other):
        return True

    def __repr__(self):
        return "memo({0})".format(self.child_node)


class IdentifierNode(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def _eq(self, other):
        return self.name == other.name

    def __repr__(self):
        return "{0}".format(self.name)


def to_node(item):
    if isinstance(item, Node):
        return item
    if isinstance(item, str):
        return StrNode(item)
    if isinstance(item, int) or isinstance(item, float):
        return NumberNode(item)
    raise FoobarException('Invalid value of type {0}'.format(type(item)))
