import networkx as nx
import copy
from CityOfBinds.src.BindGraphPublisher.node import BindFileNode
from CityOfBinds.src.BindFile.bindfile import BindFile

class BindFileGraph(nx.DiGraph):
    def __init__(self):
        super().__init__()

    def add_bind_file(self, bind_file: BindFile) -> 'BindFileGraph':
        super().add_node(self.number_of_nodes(), bind_file=copy.deepcopy(bind_file))
        return self

    def link(self, source_bind_file_index: int, target_bind_file_index: int, delay: int = 0, **condition) -> 'BindFileGraph':
        super().add_edge(source_bind_file_index, target_bind_file_index, **condition)
        if delay > 0:
            self.add_delay(source_bind_file_index, target_bind_file_index, delay)
        return self

    def chain(self, bind_file_indexes: list[int], delay: int = 0, **condition) -> 'BindFileGraph':
        for i in bind_file_indexes[:-1]:
            self.link(i, i + 1, delay=delay, **condition)
        return self

    def loop(self, bind_file_indexes: list[int], delay: int = 0, **conditions):
        self.chain(bind_file_indexes, delay=delay, **conditions)
        self.link(bind_file_indexes[-1], bind_file_indexes[0], delay=delay, **conditions)
        return self

    def make_k_regular(self, bind_file_indexes: list[int], k: int, delay: int = 0, **conditions) -> 'BindFileGraph':
        if k > len(bind_file_indexes):
            raise ValueError("k must be less than the number of bind files to create a k-regular graph.") # TODO: add verify logic (2025/11/30) 
        
        n = len(bind_file_indexes)
        for i in range(n):
            for j in range(1, k + 1):
                target_index = (i + j) % n
                self.link(bind_file_indexes[i], bind_file_indexes[target_index], delay=delay, **conditions)
        return self

    def _subdivide_edge(self, source_bind_file_index: int, target_bind_file_index: int, new_bind_file: BindFile, first_condition = None, second_condition = None) -> 'BindFileGraph':
        try:
            self.remove_edge(source_bind_file_index, target_bind_file_index)
        except nx.NetworkXError as e:
            raise ValueError(f"No link to subdivide between bind file '{self.get_bind_file(source_bind_file_index)}' and bind file '{self.get_bind_file(target_bind_file_index)}' to subdivide.") from e
        
        new_bind_file_index = self.number_of_nodes()
        self.add_bind_file(new_bind_file)
        super().add_edge(source_bind_file_index, new_bind_file_index, **(first_condition or {}))
        super().add_edge(new_bind_file_index, target_bind_file_index, **(second_condition or {}))

        return self
    
    def add_delay(self, source_bind_file_index: int, target_bind_file_index: int, steps: int = 1) -> 'BindFileGraph':
        original_trigger_conditions = self.get_trigger_conditions(source_bind_file_index, target_bind_file_index)
        original_bind_file = self.get_bind_file(source_bind_file_index)

        for _ in range(steps):
            new_delay_bind_file_index = self.number_of_nodes()
            self._subdivide_edge(
                source_bind_file_index,
                target_bind_file_index,
                original_bind_file,
                first_condition=original_trigger_conditions,
                second_condition=original_trigger_conditions
            )
            source_bind_file_index = new_delay_bind_file_index

        return self

    def get_trigger_conditions(self, source_bind_file_index: int, target_bind_file_index: int) -> dict:
        return self.get_edge_data(source_bind_file_index, target_bind_file_index) or {}

    def get_outgoing_links(self, bind_file_index: int) -> list[int]:
        return list(self.successors(bind_file_index))

    def get_incoming_links(self, bind_file_index: int) -> list[int]:
        return list(self.predecessors(bind_file_index))

    def get_bind_file(self, bind_file_index: int) -> BindFile:
        return self.nodes[bind_file_index]['bind_file']
    
