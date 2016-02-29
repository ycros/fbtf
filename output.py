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
        if isinstance(node, MemoizeNode):
            if node in self._seen_nodes:
                return FnCallNode('get', self._gen_name(node))
            else:
                self._seen_nodes[node] = self._gen_name_counter
                self._gen_name_counter += 1
                return FnCallNode('put', self._gen_name(node), self.expand(node.child_node))
        else:
            node.children = [self.expand(child) for child in node.children]
        return node


class Renderer:
    def render(self, node):
        node_type = type(node)

        if node_type is FnCallNode:
            args_output = [self.render(node) for node in node.children]
            return "${0}({1})".format(node.name.rstrip('_'), ','.join(args_output))

        if node_type is StrNode:
            return "'{0}'".format(node.value)

        if node_type is NumberNode:
            return str(node.num)

        if node_type is VarNode:
            return "%{0}%".format(node.name)

        if node_type is IdentifierNode:
            return str(node.name)

        raise FoobarOutputException('Invalid node type supplied to renderer: {0}'.format(node_type))


def output(node):
    node = MemoizationExpander().expand(node)
    return Renderer().render(node)
