import networkx as nx
import random

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

    for edge in directed_graph.edges:
        # Assign a random power to each edge
        directed_graph[edge[0]][edge[1]]['power'] = random.choice(costumes)


    return directed_graph

# Example usage
costumes = ["nemesis", "longbow", "arachnos", "warrior", "shivan", "vanguard", "skulls", "hellions"]
rw_graph = generate_random_walk_graph(costumes)

print(rw_graph.out_degree(3))

# Display the edges with their associated powers
for u, v, data in rw_graph.edges(data=True):
    print(f"{u} -> {v} [Power: {data['power']}]")
