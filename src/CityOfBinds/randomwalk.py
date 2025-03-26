import networkx as nx
import random
import csv
from CityOfBinds.binds import WASDBind
from CityOfBinds.bindfile import BindFile

def generate_random_walk_graph(costumes : list[str]):
    """ 
    Generate a directed graph with the following properties:
    - Each node has exactly 5 outbound edges.
    - Each node has at least one inbound edge.
    - A path exists between any two nodes.
    - No self-loops. (i.e., no edges from a node to itself)
    """
    node_count = len(costumes)
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

    # Add 5 copies of each costume to a new list
    costumes_extended = costumes * 5

    print(costumes_extended)

    for edge in directed_graph.edges:
        # Assign a random power to each edge
        costume = random.choice(costumes_extended)
        directed_graph[edge[0]][edge[1]]['power'] = costume
        costumes_extended.remove(costume)

    return directed_graph

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

# Create a BindFile for each costume
rw_bind_files = {}
for i in range(len(costumes)):
    rw_bind_files[i] = BindFile(filename=f"rw{i}.txt", comment_banner=f"Random Walk Node {i}", binds=[])

# Display the edges with their associated powers
for u, v, data in rw_graph.edges(data=True):
    rw_bind_files[u].binds.append(WASDBind(trigger="W", slash_commands=[f"powexectoggleon {data['power']}", f'bindloadfile {bind_folder}rw{v}.txt']))
    #print(f"{u} -> {v} [Power: {data['power']}]")

for rw_bind_file in rw_bind_files:
    wasd_triggers = ["W", "A", "S", "D", "SPACE"]
    for bind in rw_bind_files[rw_bind_file].binds:
        bind.trigger = random.choice(wasd_triggers)
        wasd_triggers.remove(bind.trigger)
    rw_bind_files[rw_bind_file].write_to_file(path="src/CityOfBinds/ex")
