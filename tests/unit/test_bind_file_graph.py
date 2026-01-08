"""
Unit tests for BindFileGraph class.

These tests focus on BindFileGraph functionality as a NetworkX DiGraph wrapper
for managing logical connections between BindFile objects.
"""

import networkx as nx
import pytest

from CityOfBinds import Bind, BindFile, BindFileGraph


class TestBindFileGraphCreation:
    """Test BindFileGraph object creation."""

    def test_empty_graph_creation(self):
        """Should create empty graph successfully."""
        graph = BindFileGraph()
        assert isinstance(graph, nx.DiGraph)
        assert len(graph.nodes) == 0
        assert len(graph.edges) == 0

    def test_inherits_networkx_methods(self):
        """Should inherit NetworkX DiGraph functionality."""
        graph = BindFileGraph()
        # Should have NetworkX methods
        assert hasattr(graph, "number_of_nodes")
        assert hasattr(graph, "number_of_edges")
        assert hasattr(graph, "successors")
        assert hasattr(graph, "predecessors")


class TestBindFileAddNodeModification:
    """Test BindFileGraph node addition."""

    def test_add_single_bind_file(self):
        """Should add single bind file as node."""
        graph = BindFileGraph()
        bf = BindFile([Bind("F1", ["say hello"])])
        # act
        graph.add_bind_file(bf)
        # assert
        assert len(graph.nodes) == 1
        assert 0 in graph.nodes  # First node should have index 0

    def test_add_multiple_bind_files(self):
        """Should add multiple bind files with sequential indexes."""
        graph = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say hello"])])
        bf2 = BindFile([Bind("F2", ["say world"])])
        bf3 = BindFile([Bind("F3", ["say test"])])
        # act
        graph.add_bind_file(bf1)
        graph.add_bind_file(bf2)
        graph.add_bind_file(bf3)
        # assert
        assert len(graph.nodes) == 3
        assert set(graph.nodes) == {0, 1, 2}

    def test_chain_add_bind_file(self):
        """Should add multiple bind files in a chain."""
        graph = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say hello"])])
        bf2 = BindFile([Bind("F2", ["say world"])])
        bf3 = BindFile([Bind("F3", ["say test"])])
        # act
        graph.add_bind_file(bf1).add_bind_file(bf2).add_bind_file(bf3)
        # assert
        assert len(graph.nodes) == 3
        assert set(graph.nodes) == {0, 1, 2}


class TestBindFileGraphLinking:
    """Test BindFileGraph link creation."""

    def test_link(self):
        """Should create basic link between two nodes."""
        graph = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say one"])])
        bf2 = BindFile([Bind("F2", ["say two"])])
        graph.add_bind_file(bf1).add_bind_file(bf2)
        # act
        graph.link(0, 1)
        # assert
        assert len(graph.edges) == 1
        assert (0, 1) in graph.edges

    def test_link_with_trigger_conditions(self):
        """Should create link with trigger conditions metadata."""
        graph = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say one"])])
        bf2 = BindFile([Bind("F2", ["say two"])])
        graph.add_bind_file(bf1).add_bind_file(bf2)
        conditions = {"on_triggers": "SPACE"}
        # act
        graph.link(0, 1, trigger_conditions=conditions)
        # assert
        stored_conditions = graph.get_trigger_conditions(0, 1)
        assert stored_conditions == conditions

    def test_multiple_links_from_one_node(self):
        """Should allow multiple outgoing links from single node."""
        graph = BindFileGraph()
        for i in range(4):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        # act
        graph.link(0, 1).link(0, 2).link(0, 3)
        # assert
        assert len(graph.edges) == 3
        outgoing = graph.get_outgoing_links(0)
        assert set(outgoing) == {1, 2, 3}

    def test_multiple_links_to_one_node(self):
        """Should allow multiple incoming links to single node."""
        graph = BindFileGraph()
        for i in range(4):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        # act
        graph.link(0, 3).link(1, 3).link(2, 3)
        # assert
        assert len(graph.edges) == 3
        incoming = graph.get_incoming_links(3)
        assert set(incoming) == {0, 1, 2}

    def test_link_with_delay(self):
        """Should create delay nodes when delay specified."""
        graph = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say one"])])
        bf2 = BindFile([Bind("F2", ["say two"])])
        graph.add_bind_file(bf1).add_bind_file(bf2)
        # act
        graph.link(0, 1, delay=2)
        # assert
        assert len(graph.nodes) == 4  # 2 original + 2 delay nodes
        assert (0, 1) not in graph.edges  # Direct link removed
        # Should have path 0 -> 2 -> 3 -> 1 (through delay nodes)
        assert (0, 2) in graph.edges
        assert (2, 3) in graph.edges
        assert (3, 1) in graph.edges


class TestBindFileGraphAdvancedLinking:
    """Test BindFileGraph advanced linking methods."""

    def test_chain_creation(self):
        """Should create linear chain of connections."""
        graph = BindFileGraph()
        for i in range(4):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        # act
        graph.chain([0, 1, 2, 3])
        # assert
        # Should create: 0->1, 1->2, 2->3
        assert len(graph.edges) == 3
        assert (0, 1) in graph.edges
        assert (1, 2) in graph.edges
        assert (2, 3) in graph.edges
        # Should not create loop back to start
        assert (3, 0) not in graph.edges

    def test_chain_with_conditions(self):
        """Should apply conditions to all chain links."""
        graph = BindFileGraph()
        for i in range(3):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        conditions = {"on_triggers": "SPACE"}
        # act
        graph.chain([0, 1, 2], trigger_conditions=conditions)
        # assert
        assert graph.get_trigger_conditions(0, 1) == conditions
        assert graph.get_trigger_conditions(1, 2) == conditions

    def test_chain_with_delay(self):
        """Should insert delay nodes between chain links."""
        graph = BindFileGraph()
        for i in range(3):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        # act
        graph.chain([0, 1, 2], delay=1)
        # assert
        # Should have 3 original + 2 delay = 5 nodes
        assert len(graph.nodes) == 5
        # Should create path 0 -> delay1 -> 1 -> delay2 -> 2
        assert (0, 3) in graph.edges  # 0 -> delay1
        assert (3, 1) in graph.edges  # delay1 -> 1
        assert (1, 4) in graph.edges  # 1 -> delay2
        assert (4, 2) in graph.edges  # delay2 -> 2

    def test_loop_creation(self):
        """Should create circular loop of connections."""
        graph = BindFileGraph()
        for i in range(4):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        # act
        graph.loop([0, 1, 2, 3])
        # assert
        # Should create: 0->1, 1->2, 2->3, 3->0 (circular)
        assert len(graph.edges) == 4
        assert (0, 1) in graph.edges
        assert (1, 2) in graph.edges
        assert (2, 3) in graph.edges
        assert (3, 0) in graph.edges  # Loop back to start

    def test_loop_with_conditions(self):
        """Should apply conditions to all loop links."""
        graph = BindFileGraph()
        for i in range(3):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        conditions = {"on_triggers": "SPACE"}
        # act
        graph.loop([0, 1, 2], trigger_conditions=conditions)
        # assert
        assert graph.get_trigger_conditions(0, 1) == conditions
        assert graph.get_trigger_conditions(1, 2) == conditions
        assert graph.get_trigger_conditions(2, 0) == conditions

    def test_loop_with_delay(self):
        """Should insert delay nodes between loop links."""
        graph = BindFileGraph()
        for i in range(3):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        # act
        graph.loop([0, 1, 2], delay=1)
        # assert
        # Should have 3 original + 3 delay = 6 nodes
        assert len(graph.nodes) == 6
        # Should create path 0 -> delay1 -> 1 -> delay2 -> 2 -> delay3 -> 0
        assert (0, 3) in graph.edges  # 0 -> delay1
        assert (3, 1) in graph.edges  # delay1 -> 1
        assert (1, 4) in graph.edges  # 1 -> delay2
        assert (4, 2) in graph.edges  # delay2 -> 2
        assert (2, 5) in graph.edges  # 2 -> delay3
        assert (5, 0) in graph.edges  # delay3 -> 0

    def test_single_node_loop(self):
        """Should create self-loop for single node."""
        graph = BindFileGraph()
        graph.add_bind_file(BindFile([Bind("F1", ["say loop"])]))
        # act
        graph.loop([0])
        # assert
        assert len(graph.edges) == 1
        assert (0, 0) in graph.edges  # Self-loop

    def test_k_regular_creation(self):
        """Should create k-regular graph structure."""
        graph = BindFileGraph()
        for i in range(5):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        # act
        graph.make_k_regular([0, 1, 2, 3, 4], k=2)
        # assert
        # Each node should have exactly 2 outgoing connections
        assert len(graph.edges) == 10  # 5 nodes * 2 connections each
        for i in range(5):
            outgoing = graph.get_outgoing_links(i)
            assert len(outgoing) == 2

    def test_k_regular_connections(self):
        """Should create correct k-regular connections."""
        graph = BindFileGraph()
        for i in range(4):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        # act
        graph.make_k_regular([0, 1, 2, 3], k=2)
        # assert
        # Check specific connections for k=2
        assert set(graph.get_outgoing_links(0)) == {1, 2}  # next 2
        assert set(graph.get_outgoing_links(1)) == {2, 3}  # next 2
        assert set(graph.get_outgoing_links(2)) == {3, 0}  # next 2 (wrapping)
        assert set(graph.get_outgoing_links(3)) == {0, 1}  # next 2 (wrapping)

    def test_k_regular_with_conditions(self):
        """Should apply conditions to all k-regular links."""
        graph = BindFileGraph()
        for i in range(4):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        conditions = {"on_triggers": "SPACE"}
        # act
        graph.make_k_regular([0, 1, 2, 3], k=2, trigger_conditions=conditions)
        # assert
        for i in range(4):
            for target in graph.get_outgoing_links(i):
                assert graph.get_trigger_conditions(i, target) == conditions

    def test_k_regular_with_delay(self):
        """Should insert delay nodes between k-regular links."""
        graph = BindFileGraph()
        for i in range(4):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        # act
        graph.make_k_regular([0, 1, 2, 3], k=2, delay=1)
        # assert
        # Each of the 4 original nodes should have 2 outgoing connections via delay nodes
        assert len(graph.nodes) == 12  # 4 original + 8 delay nodes
        for i in range(4):
            outgoing = graph.get_outgoing_links(i)
            assert len(outgoing) == 2
        for i in range(5, 12):
            # Delay nodes should each have exactly 1 outgoing connection
            assert len(graph.get_outgoing_links(i)) == 1
        assert (0, 4) in graph.edges and (4, 1) in graph.edges  # 0 -> delay1 -> 1
        assert (0, 5) in graph.edges and (5, 2) in graph.edges  # 0 -> delay2 -> 2
        assert (3, 10) in graph.edges and (10, 0) in graph.edges  # 3 -> delay7 -> 0
        assert (3, 11) in graph.edges and (11, 1) in graph.edges  # 3 -> delay8 -> 1


class TestBindFileGraphDelayOperations:
    """Test BindFileGraph delay insertion functionality."""

    def test_add_delay_single_step(self):
        """Should insert single delay node."""
        graph = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say start"])])
        bf2 = BindFile([Bind("F2", ["say end"])])
        graph.add_bind_file(bf1).add_bind_file(bf2)
        graph.link(0, 1)
        # act
        graph.add_delay(0, 1, steps=1)
        # assert
        assert len(graph.nodes) == 3  # 2 original + 1 delay
        assert (0, 1) not in graph.edges  # Direct link removed
        # Should have path 0 -> delay -> 1
        assert (0, 2) in graph.edges
        assert (2, 1) in graph.edges

    def test_add_delay_multiple_steps(self):
        """Should insert multiple delay nodes in sequence."""
        graph = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say start"])])
        bf2 = BindFile([Bind("F2", ["say end"])])
        graph.add_bind_file(bf1).add_bind_file(bf2)
        graph.link(0, 1)
        # act
        graph.add_delay(0, 1, steps=3)
        # assert
        assert len(graph.nodes) == 5  # 2 original + 3 delay
        assert (0, 1) not in graph.edges  # Direct link removed
        # Should create path 0 -> delay1 -> delay2 -> delay3 -> 1
        assert (0, 2) in graph.edges
        assert (2, 3) in graph.edges
        assert (3, 4) in graph.edges
        assert (4, 1) in graph.edges

    def test_delay_preserves_trigger_conditions(self):
        """Should preserve trigger conditions through delay nodes."""
        graph = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say start"])])
        bf2 = BindFile([Bind("F2", ["say end"])])
        graph.add_bind_file(bf1).add_bind_file(bf2)
        conditions = {"on_triggers": "SPACE"}
        graph.link(0, 1, trigger_conditions=conditions)
        # act
        graph.add_delay(0, 1, steps=1)
        # assert
        assert graph.get_trigger_conditions(0, 2) == conditions
        assert graph.get_trigger_conditions(2, 1) == conditions

    def test_delay_uses_source_bind_file_copy(self):
        """Should use copy of source bind file for delay nodes."""
        graph = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say original"])])
        bf2 = BindFile([Bind("F2", ["say target"])])
        graph.add_bind_file(bf1).add_bind_file(bf2)
        graph.link(0, 1)

        graph.add_delay(0, 1, steps=1)

        outgoing_from_0 = graph.get_outgoing_links(0)
        delay_node = outgoing_from_0[0]
        delay_bind_file = graph.get_bind_file(delay_node)
        original_bind_file = graph.get_bind_file(0)

        # Delay node should have copy of original bind file
        assert len(delay_bind_file.binds) == len(original_bind_file.binds)
        assert str(delay_bind_file.binds[0]) == str(original_bind_file.binds[0])


class TestBindFileGraphQueries:
    """Test BindFileGraph query methods."""

    def test_get_bind_file(self):
        """Should retrieve stored bind files by index."""
        graph = BindFileGraph()
        original_bf = BindFile([Bind("F1", ["say hello"])])
        graph.add_bind_file(original_bf)
        # act
        retrieved_bf = graph.get_bind_file(0)
        # assert
        assert isinstance(retrieved_bf, BindFile)
        assert len(retrieved_bf.binds) == 1
        assert str(retrieved_bf.binds[0]) == 'F1 "say hello"'

    def test_get_trigger_conditions_exists(self):
        """Should return trigger conditions when they exist."""
        graph = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say one"])])
        bf2 = BindFile([Bind("F2", ["say two"])])
        graph.add_bind_file(bf1).add_bind_file(bf2)
        conditions = {"on_triggers": "SPACE", "timing": "instant"}
        graph.link(0, 1, trigger_conditions=conditions)
        # act
        result = graph.get_trigger_conditions(0, 1)
        # assert
        assert result == conditions

    def test_get_trigger_conditions_empty(self):
        """Should return empty dict when no conditions set."""
        graph = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say one"])])
        bf2 = BindFile([Bind("F2", ["say two"])])
        graph.add_bind_file(bf1).add_bind_file(bf2)
        graph.link(0, 1)  # No conditions
        # act
        result = graph.get_trigger_conditions(0, 1)
        # assert
        assert result == {}

    def test_get_outgoing_links(self):
        """Should return all nodes this node links to."""
        graph = BindFileGraph()
        for i in range(4):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))

        graph.link(0, 1).link(0, 2).link(1, 3)

        assert set(graph.get_outgoing_links(0)) == {1, 2}
        assert set(graph.get_outgoing_links(1)) == {3}
        assert set(graph.get_outgoing_links(2)) == set()  # No outgoing links
        assert set(graph.get_outgoing_links(3)) == set()  # No outgoing links

    def test_get_incoming_links(self):
        """Should return all nodes that link to this node."""
        graph = BindFileGraph()
        for i in range(4):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))

        graph.link(0, 2).link(1, 2).link(2, 3)

        assert set(graph.get_incoming_links(0)) == set()  # No incoming links
        assert set(graph.get_incoming_links(1)) == set()  # No incoming links
        assert set(graph.get_incoming_links(2)) == {0, 1}
        assert set(graph.get_incoming_links(3)) == {2}


class TestBindFileGraphValidation:
    """Test BindFileGraph validation and error handling."""

    def test_subdivide_edge_nonexistent_edge(self):
        """Should raise error when trying to subdivide nonexistent edge."""
        graph = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say one"])])
        bf2 = BindFile([Bind("F2", ["say two"])])
        bf3 = BindFile([Bind("F3", ["say three"])])
        graph.add_bind_file(bf1).add_bind_file(bf2).add_bind_file(bf3)

        # Try to subdivide edge that doesn't exist
        with pytest.raises(ValueError, match="No link to subdivide"):
            graph._subdivide_edge(0, 1, bf3)

    def test_k_regular_validation(self):
        """Should validate k-regular parameters."""
        graph = BindFileGraph()
        for i in range(3):
            graph.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))

        # k >= number of nodes should raise error
        with pytest.raises(
            ValueError, match="k must be less than the number of bind files"
        ):
            graph.make_k_regular([0, 1, 2], k=3)


class TestBindFileGraphExtend:
    """Test BindFileGraph extend functionality."""

    def test_extend_without_merging(self):
        """Should extend graph with offset node IDs and preserved edges."""
        # Setup first graph
        bfg1 = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say one"])])
        bf2 = BindFile([Bind("F2", ["say two"])])
        bfg1.add_bind_file(bf1).add_bind_file(bf2)
        bfg1.link(0, 1)

        # Setup second graph
        bfg2 = BindFileGraph()
        bf3 = BindFile([Bind("F3", ["say three"])])
        bf4 = BindFile([Bind("F4", ["say four"])])
        bfg2.add_bind_file(bf3).add_bind_file(bf4)
        bfg2.link(0, 1)

        # act
        bfg1.extend(bfg2)

        # assert
        assert len(bfg1.nodes) == 4  # 2 + 2
        assert set(bfg1.nodes) == {0, 1, 2, 3}
        assert len(bfg1.edges) == 2  # Original edge + extended edge
        assert (0, 1) in bfg1.edges  # Original edge preserved
        assert (2, 3) in bfg1.edges  # Extended edge with offset IDs

    def test_extend_with_single_merge(self):
        """Should merge specified nodes and combine their edges."""
        # Setup first graph
        bfg1 = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say one"])])
        bf2 = BindFile([Bind("F2", ["say two"])])
        bfg1.add_bind_file(bf1).add_bind_file(bf2)
        bfg1.link(0, 1)

        # Setup second graph
        bfg2 = BindFileGraph()
        bf3 = BindFile([Bind("F2", ["say two"])])
        bf4 = BindFile([Bind("F3", ["say three"])])
        bfg2.add_bind_file(bf3).add_bind_file(bf4)
        bfg2.link(0, 1)

        # act - merge node 1 from bfg1 with node 0 from bfg2
        bfg1.extend(bfg2, merge_on=[(1, 0)])

        # assert
        assert len(bfg1.nodes) == 3  # 2 + 2 - 1 (merged node)
        assert set(bfg1.nodes) == {0, 1, 2}
        assert len(bfg1.edges) == 2  # Original edge + extended edge
        assert (0, 1) in bfg1.edges  # Original edge preserved
        assert (1, 2) in bfg1.edges  # Extended edge now points from merged node

    def test_extend_preserves_trigger_conditions(self):
        """Should preserve trigger conditions during extend."""
        # Setup first graph
        bfg1 = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say one"])])
        bf2 = BindFile([Bind("F2", ["say two"])])
        bfg1.add_bind_file(bf1).add_bind_file(bf2)
        conditions1 = {"on_triggers": "F1"}
        bfg1.link(0, 1, trigger_conditions=conditions1)

        # Setup second graph with different conditions
        bfg2 = BindFileGraph()
        bf3 = BindFile([Bind("F3", ["say three"])])
        bf4 = BindFile([Bind("F4", ["say four"])])
        bfg2.add_bind_file(bf3).add_bind_file(bf4)
        conditions2 = {"on_triggers": "SPACE"}
        bfg2.link(0, 1, trigger_conditions=conditions2)

        # act
        bfg1.extend(bfg2)

        # assert
        assert bfg1.get_trigger_conditions(0, 1) == conditions1
        assert bfg1.get_trigger_conditions(2, 3) == conditions2

    def test_extend_with_multiple_merges(self):
        """Should handle multiple node merges correctly."""
        # Setup first graph with 3 nodes
        bfg1 = BindFileGraph()
        for i in range(3):
            bfg1.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        bfg1.loop([0, 1, 2])  # 0->1->2->0

        # Setup second graph with 3 nodes
        bfg2 = BindFileGraph()
        for i in range(3):
            bfg2.add_bind_file(BindFile([Bind(f"{i+1}", [f"say g{i+1}"])]))
        bfg2.chain([0, 1, 2])  # 0->1->2

        # act - merge (1,0) and (2,1)
        bfg1.extend(bfg2, merge_on=[(1, 0), (2, 1)])

        # assert
        assert len(bfg1.nodes) == 4  # 3 + 3 - 2 (two merged nodes)
        assert set(bfg1.nodes) == {0, 1, 2, 3}
        # Original edges: 0->1, 1->2, 2->0
        # Extended edges: merged(1,0)->merged(2,1), merged(2,1)->node3
        # Result: 0->1, 1->2, 2->0, 1->2, 2->3
        assert (0, 1) in bfg1.edges
        assert (1, 2) in bfg1.edges
        assert (2, 0) in bfg1.edges
        assert (2, 3) in bfg1.edges  # merged(2,1) -> node3

    def test_extend_preserves_bind_files_on_merge(self):
        """Should keep original bind files when merging nodes."""
        # Setup graphs
        bfg1 = BindFileGraph()
        original_bind = Bind("F1", ["say original"])
        bf1 = BindFile([original_bind])
        bfg1.add_bind_file(bf1)

        bfg2 = BindFileGraph()
        other_bind = Bind("F2", ["say other"])
        bf2 = BindFile([other_bind])
        bfg2.add_bind_file(bf2)

        # act
        bfg1.extend(bfg2, merge_on=[(0, 0)])

        # assert - should keep bfg1's bind file
        merged_bind_file = bfg1.get_bind_file(0)
        assert len(merged_bind_file.binds) == 1
        assert str(merged_bind_file.binds[0]) == 'F1 "say original"'

    def test_extend_empty_graph(self):
        """Should handle extending with empty graph."""
        bfg1 = BindFileGraph()
        bfg1.add_bind_file(BindFile([Bind("F1", ["say hello"])]))

        bfg2 = BindFileGraph()  # Empty

        # act
        bfg1.extend(bfg2)

        # assert
        assert len(bfg1.nodes) == 1  # No change
        assert len(bfg1.edges) == 0  # No change

    def test_extend_to_empty_graph(self):
        """Should handle extending empty graph with non-empty graph."""
        bfg1 = BindFileGraph()  # Empty

        bfg2 = BindFileGraph()
        bf1 = BindFile([Bind("F1", ["say hello"])])
        bf2 = BindFile([Bind("F2", ["say world"])])
        bfg2.add_bind_file(bf1).add_bind_file(bf2)
        bfg2.link(0, 1)

        # act
        bfg1.extend(bfg2)

        # assert
        assert len(bfg1.nodes) == 2  # 0 + 2
        assert len(bfg1.edges) == 1  # 0 + 1
        assert (0, 1) in bfg1.edges

    def test_extend_complex_topology(self):
        """Should handle extending graphs with complex topologies."""
        # Setup k-regular graph
        bfg1 = BindFileGraph()
        for i in range(4):
            bfg1.add_bind_file(BindFile([Bind(f"F{i+1}", [f"say {i+1}"])]))
        bfg1.make_k_regular([0, 1, 2, 3], k=2)

        # Setup loop graph
        bfg2 = BindFileGraph()
        for i in range(3):
            bfg2.add_bind_file(BindFile([Bind(f"{i+1}", [f"say g{i+1}"])]))
        bfg2.loop([0, 1, 2])

        # act
        bfg1.extend(bfg2)

        # assert
        assert len(bfg1.nodes) == 7  # 4 + 3
        assert len(bfg1.edges) == 11  # 8 (k-regular) + 3 (loop)
        # Check that k-regular structure is preserved
        for i in range(4):
            assert len(bfg1.get_outgoing_links(i)) == 2
        # Check that loop structure is preserved (with offset)
        assert set(bfg1.get_outgoing_links(4)) == {5}  # 0+4 -> 1+4
        assert set(bfg1.get_outgoing_links(5)) == {6}  # 1+4 -> 2+4
        assert set(bfg1.get_outgoing_links(6)) == {4}  # 2+4 -> 0+4

    def test_extend_chain_returns_self(self):
        """Should return self for method chaining."""
        bfg1 = BindFileGraph()
        bfg1.add_bind_file(BindFile([Bind("F1", ["say hello"])]))

        bfg2 = BindFileGraph()
        bfg2.add_bind_file(BindFile([Bind("F2", ["say world"])]))

        # act
        result = bfg1.extend(bfg2)

        # assert
        assert result is bfg1
