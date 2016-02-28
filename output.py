from nodes import MemoizeNode, FnCallNode, to_node


class MemoizationExpander:
    def __init__(self):
        self._gen_name_counter = 0
        self._seen_nodes = {}

    def _gen_name(self, node, counter=None):
        if counter is None:
            counter = self._seen_nodes[node]
        to_node('v{0}'.format(counter))

    def expand(self, node):
        if isinstance(node, MemoizeNode):
            if node in self._seen_nodes:
                return FnCallNode('get', self._gen_name(node))
            else:
                self._seen_nodes[node] = self._gen_name_counter
                self._gen_name_counter += 1
                return FnCallNode('put', self._gen_name(node), node.child_node)
        else:
            node.children = [self.expand(child) for child in node.children]
        return node


# class Renderer:
#     def __init__(self):
#         pass
#
#     def render(self, node):
#         node_type = type(node)
#         if node_type is FnCallNode()


def output(node):
    node = MemoizationExpander().expand(node)
    return node.output()
