import networkx as nx
import copy
from CityOfBinds.src.BindGraphPublisher.node import BindFileNode
from CityOfBinds.src.BindFile.bindfile import BindFile

class BindFileGraph(nx.DiGraph):
    def __init__(self):
        super().__init__()

    def add_node(self, node: BindFileNode) -> 'BindFileGraph':
        super().add_node(node.id, bind_file=copy.deepcopy(node.bind_file))
        return self
    
    def add_edge(self, from_node: BindFileNode, to_node: BindFileNode, **condition) -> 'BindFileGraph':
        self.add_node(from_node)
        self.add_node(to_node)

        super().add_edge(from_node.id, to_node.id, **condition)
        return self

    def chain_nodes(self, node_list: list[BindFileNode], close_loop = False, **condition) -> 'BindFileGraph':
        for i in range(len(node_list) - 1):
            self.add_edge(node_list[i], node_list[i + 1], **condition)

        if close_loop and len(node_list) > 1:
            self.add_edge(node_list[-1], node_list[0], **condition)

        return self

    def subdivide_edge(self, from_node: BindFileNode, to_node: BindFileNode, new_node: BindFileNode, first_condition = None, second_condition = None) -> 'BindFileGraph':
        if not self.has_edge(from_node.id, to_node.id):
            raise ValueError(f"Edge from node {from_node.id} to node {to_node.id} does not exist.")

        self.remove_edge(from_node.id, to_node.id)
        self.add_node(new_node)
        super().add_edge(from_node.id, new_node.id, **(first_condition or {}))
        super().add_edge(new_node.id, to_node.id, **(second_condition or {}))

        return self

    def add_delay(self, from_node: BindFileNode, to_node: BindFileNode, steps: int = 1) -> 'BindFileGraph':
        for _ in range(steps):
            delay_node = BindFileNode(self.number_of_nodes(), from_node.bind_file)
            self.subdivide_edge(from_node, to_node, delay_node)
            from_node = delay_node
        return self

    def get_bind_file(self, node_id: int) -> BindFile:
        return self.nodes[node_id]['bind_file']

    def get_node_by_id(self, node_id: int) -> BindFileNode:
        return BindFileNode(node_id, self.get_bind_file(node_id))
