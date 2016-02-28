from abc import ABCMeta, abstractmethod
from exceptions import FoobarException


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
        return FnCallNode(item, self)

    def _add_child(self, child_node):
        if not isinstance(child_node, Node):
            raise FoobarException('Attempted to add a non-node as a child.')
        self.children.append(child_node)

    @abstractmethod
    def __hash__(self):
        result = super().__hash__()
        for child in self.children:
            result ^= hash(child)
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

    def output(self):
        args_output = [x.output() for x in self.children]
        return "${0}({1})".format(self.name.lstrip('_'), ','.join(args_output))

    def __hash__(self):
        return super().__hash__() ^ hash(self.name)

    def _eq(self, other):
        return other.name == self.name


class StrNode(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def output(self):
        return "'{0}'".format(self.value)

    def __hash__(self):
        return hash(self.value)

    def _eq(self, other):
        return other.value == self.value


class NumberNode(Node):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def output(self):
        return "{0}".format(self.num)

    def __hash__(self):
        return hash(self.num)

    def _eq(self, other):
        return other.num == self.num


class VarNode(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def output(self):
        return "%{0}%".format(self.name)

    def __hash__(self):
        return hash(self.name)

    def _eq(self, other):
        return other.name == self.name


class MemoizeNode(Node):
    def __init__(self, child_node):
        super().__init__()
        self.child_node = child_node
        self._add_child(child_node)

    def output(self):
        raise FoobarException()

    def __hash__(self):
        return super().__hash__()

    def _eq(self, other):
        return True


class IdentifierNode(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def _eq(self, other):
        return self.name == other.name


def to_node(item):
    if isinstance(item, Node):
        return item
    if isinstance(item, str):
        return StrNode(item)
    if isinstance(item, int) or isinstance(item, float):
        return NumberNode(item)
    raise FoobarException('Invalid value of type {0}'.format(type(item)))