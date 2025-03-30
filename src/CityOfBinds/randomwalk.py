import networkx as nx
import random
import csv
from CityOfBinds.binds import WASDBind
from CityOfBinds.bindfile import BindFile

class RandomWalk:
    def __init__(self,  slash_commands: list[str], file_prefix: str = "", bind_banner: str = ""):
        self._slash_commands = slash_commands
        self._bind_banner = bind_banner
        self._file_prefix = file_prefix
        self._rw_graph = None

        self.slash_commands = slash_commands
        self.bind_banner = bind_banner
        self.file_prefix = file_prefix

    @property
    def slash_commands(self) -> list[str]:
        return self._slash_commands
    
    @slash_commands.setter
    def slash_commands(self, slash_commands: list[str]):
        self._slash_commands = slash_commands
        self._rw_graph = self._generate_random_walk_graph(slash_commands)

    def _generate_random_walk_graph(self, slash_commands : list[str]) -> nx.DiGraph:
        """ 
        Generate a directed graph with the following properties:
        - Each node has exactly 5 outbound edges.
        - Each node has at least one inbound edge.
        - A path exists between any two nodes.
        - No self-loops. (i.e., no edges from a node to itself)
        """
        node_count = len(slash_commands)
        directed_graph = nx.DiGraph()

        # Add nodes
        for node in range(node_count):
            directed_graph.add_node(node)

        # Ensure a path exists btween any two nodes and each node has at least one inbound edge.
        for node in directed_graph.nodes:
            directed_graph.add_edge(node, (node + 1) % node_count)

        # Ensure each node has 5 outbound edges and that there are no self-loops.
        for node in directed_graph.nodes:
            while directed_graph.out_degree(node) < 5:
                target = random.choice(list(set(range(node_count)) - {node}))
                directed_graph.add_edge(node, target)

        # Add 5 copies of each slash command to a new list
        slash_commands_extended = slash_commands * 5

        for edge in directed_graph.edges:
            # Assign a random slash_command to each edge
            slash_command = random.choice(slash_commands_extended)
            directed_graph[edge[0]][edge[1]]['slash_command'] = slash_command
            slash_commands_extended.remove(slash_command)

        return directed_graph

    def publish_files(self, path: str = ''):
        """Write all the binds to the file."""

        # Create a BindFile for each slash_command
        rw_bind_files = {}
        for i in range(len(self._rw_graph.nodes)):
            rw_bind_files[i] = BindFile(filename=f"{self.file_prefix}{i}.txt", comment_banner=f"{self.bind_banner} {i}", binds=[])

        # Display the edges with their associated powers
        for u, v, data in rw_graph.edges(data=True):
            rw_bind_files[u].binds.append(WASDBind(trigger="W", slash_commands=[f"{data['slash_command']}", f'bindloadfile {path}{self.file_prefix}{v}.txt'])) # TODO: fix path
            #print(f"{u} -> {v} [Power: {data['power']}]")

        for rw_bind_file in rw_bind_files:
            wasd_triggers = ["W", "A", "S", "D", "SPACE"]
            for bind in rw_bind_files[rw_bind_file].binds:
                bind.trigger = random.choice(wasd_triggers)
                wasd_triggers.remove(bind.trigger)
            rw_bind_files[rw_bind_file].write_to_file(path="src/CityOfBinds/ex")




def read_costumes_from_csv(file_path: str) -> list[str]:
    """Read costumes from a CSV file."""
    costumes = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            costumes.extend(row)
    return costumes

# Example usage
#costumes = ["nemesis", "longbow", "arachnos", "warrior", "shivan", "vanguard", "skulls", "hellions"]
costumes = read_costumes_from_csv("src/CityOfBinds/costumes.csv")
bind_folder = "D:/CoH/b/ms/rw/"
rw_graph = generate_random_walk_graph(costumes)


