import copy

import networkx as nx

from ...configs.constants import BFGConstants
from ...game.bind_file.bind_file import BindFile


class BindFileGraph(nx.DiGraph):
    """
    A wrapper around NetworkX DiGraph for managing logical connections between BindFile objects.

    This class enables the creation of complex rotating bind patterns by establishing directed
    relationships between bind files with optional trigger conditions and delays.

    Terminology:
        - Link: A directed connection from a source bind file to a target bind file
        - Trigger Conditions: Optional metadata describing when/how bind files are connected
        - Node Index: Integer identifier for each bind file in the graph (auto-assigned)
        - Edge: The connection between two bind files with optional trigger conditions

    Common Patterns:
        - Chain: bf1 -> bf2 -> bf3 (linear sequence)
        - Loop: bf1 -> bf2 -> bf3 -> bf1 (circular sequence)
        - K-Regular: Each bind file connects to k other bind files
    """

    def add_bind_file(self, bind_file: BindFile) -> "BindFileGraph":
        """
        Add a copy of a BindFile as a new node in the graph.

        Args:
            bind_file: The BindFile to add to the graph

        Returns:
            Self for method chaining

        Example:
            >>> graph = BindFileGraph()
            >>> bf1 = BindFile([Bind("F1", ["say hello"])])
            >>> graph.add_bind_file(bf1)  # Node 0
            >>> len(graph.nodes)  # 1
        """
        # Use deep copy to prevent mutating original BindFile during graph operations
        super().add_node(self.number_of_nodes(), bind_file=copy.deepcopy(bind_file))
        return self

    def link(
        self,
        source_bind_file_index: int,
        target_bind_file_index: int,
        trigger_conditions: dict = None,
        delay: int = 0,
    ) -> "BindFileGraph":
        """
        Create a directed link from source to target bind file.

        Args:
            source_bind_file_index: Index of the source bind file
            target_bind_file_index: Index of the target bind file
            trigger_conditions: Optional conditions for what triggers this link
            delay: Number of copies of source node and intermediate links to insert as delay

        Returns:
            Self for method chaining

        Example:
            >>> graph.link(0, 1)  # bf0 -> bf1
            >>> graph.link(0, 2, {"on_triggers": "SPACE"})  # bf0 -> bf2 (on SPACE press only)
            >>> graph.link(1, 2, delay=2)  # bf1 -> copy(bf1) -> copy(bf1) -> bf2
        """
        # Add the edge with trigger conditions as metadata
        super().add_edge(
            source_bind_file_index,
            target_bind_file_index,
            **{BFGConstants.EDGE_DATA_KEY: trigger_conditions} or {},
        )
        # Insert delay nodes if requested
        if delay > 0:
            self.add_delay(source_bind_file_index, target_bind_file_index, delay)
        return self

    def chain(
        self,
        bind_file_indexes: list[int],
        trigger_conditions: dict = None,
        delay: int = 0,
    ) -> "BindFileGraph":
        """
        Create a linear chain of bind files in sequence.

        Args:
            bind_file_indexes: List of node indexes to chain in list order
            trigger_conditions: Conditions applied to all links in the chain
            delay: Delay applied to all links in the chain

        Returns:
            Self for method chaining

        Example:
            >>> graph.chain([0, 1, 2])  # Creates: bf0 -> bf1 -> bf2
            >>> graph.chain([4, 3, 5], {"on_triggers": "F1"})  # bf4 -> bf3 -> bf5 (all on F1)
        """
        # Link each consecutive pair in the sequence
        for i in bind_file_indexes[:-1]:
            self.link(i, i + 1, trigger_conditions=trigger_conditions, delay=delay)
        return self

    def loop(
        self,
        bind_file_indexes: list[int],
        trigger_conditions: dict = None,
        delay: int = 0,
    ) -> "BindFileGraph":
        """
        Create a circular loop connecting bind files in list order, with last linking back to first.

        Args:
            bind_file_indexes: List of node indexes to connect in a loop
            trigger_conditions: Conditions applied to all links in the loop
            delay: Delay applied to all links in the loop

        Returns:
            Self for method chaining

        Example:
            >>> graph.loop([0, 1, 2])  # Creates: bf0 -> bf1 -> bf2 -> bf0 (circular)
            >>> graph.loop([6, 4, 5, 3])  # bf6 -> bf4 -> bf5 -> bf3 -> bf6 (circular)
        """
        # Handle empty list case
        if not bind_file_indexes:
            return self

        # Create the chain first
        self.chain(
            bind_file_indexes, trigger_conditions=trigger_conditions, delay=delay
        )
        # Connect the last back to the first to complete the loop
        self.link(
            bind_file_indexes[-1],
            bind_file_indexes[0],
            trigger_conditions=trigger_conditions,
            delay=delay,
        )
        return self

    def make_k_regular(
        self,
        bind_file_indexes: list[int],
        k: int,
        trigger_conditions: dict = None,
        delay: int = 0,
    ) -> "BindFileGraph":
        """
        Create a k-regular graph where each bind file connects to exactly k other bind files.

        In a k-regular graph, every node has exactly k outgoing edges. Connections are made
        to the next k nodes in circular/list order.

        Args:
            bind_file_indexes: List of node indexes to make k-regular
            k: Number of outgoing connections each node should have
            trigger_conditions: Conditions applied to all links
            delay: Delay applied to all links

        Returns:
            Self for method chaining

        Raises:
            ValueError: If k >= number of bind files (impossible to create without self links)

        Example:
            >>> graph.make_k_regular([0, 1, 2, 3], k=2)
            # Creates: bf0 -> bf1, bf2
            #          bf1 -> bf2, bf3
            #          bf2 -> bf3, bf0
            #          bf3 -> bf0, bf1
        """
        if k >= len(bind_file_indexes):
            raise ValueError(
                "k must be less than the number of bind files to create a k-regular graph."
            )

        n = len(bind_file_indexes)
        # For each node, connect to the next k nodes in circular order
        for i in range(n):
            for j in range(1, k + 1):
                target_index = (i + j) % n  # Wrap around using modulo
                self.link(
                    bind_file_indexes[i],
                    bind_file_indexes[target_index],
                    trigger_conditions=trigger_conditions,
                    delay=delay,
                )
        return self

    def _subdivide_edge(
        self,
        source_bind_file_index: int,
        target_bind_file_index: int,
        new_bind_file: BindFile,
        first_condition=None,
        second_condition=None,
    ) -> "BindFileGraph":
        """
        Internal method to subdivide an existing edge by inserting a new node.

        Removes the direct edge between source and target, then creates:
        source -> new_node -> target

        Args:
            source_bind_file_index: Starting node
            target_bind_file_index: Ending node
            new_bind_file: BindFile to insert as intermediate node
            first_condition: Trigger conditions for source -> new_node
            second_condition: Trigger conditions for new_node -> target

        Returns:
            Self for method chaining

        Raises:
            ValueError: If no edge exists between source and target
        """
        # Remove the existing direct edge
        try:
            self.remove_edge(source_bind_file_index, target_bind_file_index)
        except nx.NetworkXError as e:
            raise ValueError(
                f"No link to subdivide between bind file '{self.get_bind_file(source_bind_file_index)}' and bind file '{self.get_bind_file(target_bind_file_index)}'."
            ) from e

        # Add the new intermediate node
        new_bind_file_index = self.number_of_nodes()
        self.add_bind_file(new_bind_file)

        # Create the two new edges: source -> new -> target
        super().add_edge(
            source_bind_file_index,
            new_bind_file_index,
            **(
                {BFGConstants.EDGE_DATA_KEY: first_condition} if first_condition else {}
            ),
        )
        super().add_edge(
            new_bind_file_index,
            target_bind_file_index,
            **(
                {BFGConstants.EDGE_DATA_KEY: second_condition}
                if second_condition
                else {}
            ),
        )

        return self

    def add_delay(
        self, source_bind_file_index: int, target_bind_file_index: int, steps: int = 1
    ) -> "BindFileGraph":
        """
        Insert copies of source node between two connected nodes. Maintains trigger conditions.

        This method subdivides an existing edge by inserting intermediate nodes,
        effectively creating a delay in the bind file sequence.

        Args:
            source_bind_file_index: Starting node index
            target_bind_file_index: Ending node index
            steps: Number of delay nodes to insert

        Returns:
            Self for method chaining

        Example:
            >>> graph.link(0, 1)  # bf0 -> bf1
            >>> graph.add_delay(0, 1, 2)  # bf0 -> copy(bf0) -> copy(bf0) -> bf1
        """
        # Preserve the original connection conditions
        original_trigger_conditions = self.get_trigger_conditions(
            source_bind_file_index, target_bind_file_index
        )
        original_bind_file = self.get_bind_file(source_bind_file_index)

        # Insert the specified number of delay nodes
        for _ in range(steps):
            new_delay_bind_file_index = self.number_of_nodes()
            self._subdivide_edge(
                source_bind_file_index,
                target_bind_file_index,
                original_bind_file,
                first_condition=original_trigger_conditions,
                second_condition=original_trigger_conditions,
            )
            # Update source for next iteration (chaining delays)
            source_bind_file_index = new_delay_bind_file_index

        return self

    def get_trigger_conditions(
        self, source_bind_file_index: int, target_bind_file_index: int
    ) -> dict:
        """Get the trigger conditions for a specific edge.

        Args:
            source_bind_file_index: Source node index
            target_bind_file_index: Target node index

        Returns:
            Dictionary of trigger conditions, empty dict if none set
        """
        return (
            self.get_edge_data(source_bind_file_index, target_bind_file_index)[
                BFGConstants.EDGE_DATA_KEY
            ]
            or {}
        )

    def get_outgoing_links(self, bind_file_index: int) -> list[int]:
        """Get all node indexes that this bind file links to.

        Args:
            bind_file_index: Node index to get outgoing links for

        Returns:
            List of target node indexes
        """
        return list(self.successors(bind_file_index))

    def get_incoming_links(self, bind_file_index: int) -> list[int]:
        """Get all node indexes that link to this bind file.

        Args:
            bind_file_index: Node index to get incoming links for

        Returns:
            List of source node indexes
        """
        return list(self.predecessors(bind_file_index))

    def get_bind_file(self, bind_file_index: int) -> BindFile:
        """Retrieve the BindFile object stored at a specific node.

        Args:
            bind_file_index: Node index to retrieve BindFile from

        Returns:
            BindFile object stored at the specified node
        """
        return self.nodes[bind_file_index][BFGConstants.NODE_DATA_KEY]
