from copy import copy

from exceptions import FoobarException
from nodes import MemoizeNode, FnCallNode, StrNode, NumberNode, VarNode, IdentifierNode


class FoobarOutputException(FoobarException):
    pass


class MemoizationExpander:
    def __init__(self):
        self._gen_name_counter = 0
        self._seen_nodes = {}

    def _gen_name(self, node, counter=None):
        if counter is None:
            counter = self._seen_nodes[node]
        return IdentifierNode('v{0}'.format(counter))

    def expand(self, node):
        node = copy(node)
        if isinstance(node, MemoizeNode):
            if node in self._seen_nodes:
                return FnCallNode('get', self._gen_name(node))
            else:
                self._seen_nodes[node] = self._gen_name_counter
                self._gen_name_counter += 1
                return FnCallNode('put', self._gen_name(node), self.expand(node.child_node))
        node.children = [self.expand(child) for child in node.children]
        return node


class Optimizer:
    def __init__(self):
        self._gen_name_counter = -1
        self._node_count = {}
        self._pass2_seen_nodes = {}
        self._renderer = Renderer()

    @staticmethod
    def _gen_name(counter):
        return IdentifierNode('v{0}'.format(counter))

    def optimize(self, node):
        self._pass1(node)
        return self._pass2(node)

    def _pass1(self, node):
        # TODO: coupled to logic in _should_optimize method, refactor me.
        try:
            self._node_count[node] += 1
        except KeyError:
            self._node_count[node] = 1
            # only consider children if parent isn't already going to be optimized away.
            for child in node.children:
                self._pass1(child)

    def _pass2(self, node, skip_child=False):
        node = copy(node)
        seen_val = self._node_count[node]
        if self._should_optimize(node, seen_val) and not skip_child:
            try:
                counter = self._pass2_seen_nodes[node]
                return FnCallNode('get', self._gen_name(counter))
            except KeyError:
                self._gen_name_counter += 1
                self._pass2_seen_nodes[node] = self._gen_name_counter
                return FnCallNode('put', self._gen_name(self._gen_name_counter), self._pass2(node, True))
        node.children = [self._pass2(child) for child in node.children]
        return node

    @staticmethod
    def _should_optimize(node, seen_val):
        if seen_val > 1:
            if len(node.children) > 0:
                # if type(node) != FnCallNode or node.name not in ('get', 'put', 'puts'):
                # TODO: estimate generated code length?
                return True
        return False


class Renderer:
    def __init__(self, pretty=False):
        self.pretty = pretty
        self._indent_level = 0

    def render(self, node, indent_level=1):
        node_type = type(node)

        if node_type is FnCallNode:
            args_output = [self.render(node, indent_level=indent_level+1) for node in node.children]
            normal_format = "${0}({1})".format(node.name.rstrip('_'), ','.join(args_output))
            if self.pretty:
                indent = indent_level * '  '
                if len(normal_format) > 40 or len(normal_format) + len(indent) > 60:
                    return "${0}(\n{2}{1})".format(node.name.rstrip('_'), (',\n'+indent).join(args_output), indent)
            return normal_format

        if node_type is StrNode:
            return "'{0}'".format(node.value)

        if node_type is NumberNode:
            return str(node.num)

        if node_type is VarNode:
            return "%{0}%".format(node.name)

        if node_type is IdentifierNode:
            return str(node.name)

        raise FoobarOutputException('Invalid node type supplied to renderer: {0}'.format(node_type))


def output(node, pretty=False, optimize=True):
    node = MemoizationExpander().expand(node)
    if optimize:
        node = Optimizer().optimize(node)
    return Renderer(pretty).render(node)
