from enum import Enum
from typing import List, Optional
from wsgiref.simple_server import WSGIServer

from setuptools.command.build_ext import if_dl

from dictionaries.dictionary import Dictionary
from dictionaries.term_dictionary import TermDictionaryEntry

class NodeType(Enum):
    BOS = 0,
    EOS = 1,
    TERM = 2

class LatticeNode:
    def __init__(self, start_index: int, end_index: int, term_id: int, node_type: NodeType = NodeType.TERM, term: str = ""):
        self.node_type: NodeType = node_type
        
        self.start_index: int = start_index  # The starting position of this node in the lattice, zero-indexed
        self.end_index: int = end_index      # The ending position of this node in the lattice, zero-indexed
        
        self.term: str = term
        self.term_id: int = term_id          # The associated term ID of this node. This is simply an index into the dictionary
        
        self.total_cost: Optional[int] = None          # The total cost associated with this node, this is used when calculating the optimal path through the lattice
        self.previous_node: Optional[LatticeNode] = None
        
    def __str__(self) -> str:
        if self.node_type == NodeType.TERM:
            return f"{self.term} ({self.term_id}) [{self.start_index}-{self.end_index}]"
        elif self.node_type == NodeType.BOS:
            return "BOS"
        else:
            return "EOS"
    
    def __repr__(self) -> str:
        return str(self)
        
class Lattice:
    def __init__(self, dictionary: Dictionary, nodes: List[LatticeNode] = None):
        self.dictionary: Dictionary = dictionary
        self.nodes: List[LatticeNode] = nodes if nodes is not None else []
       
        if nodes is not None: 
            self.length: int = max(node.end_index for node in self.nodes)
        else:
            self.length: int = 0
            
    def __str__(self) -> str:
        string_representation = ""
        for node in self.nodes:
            if node.node_type == NodeType.TERM:
                string_representation += f"{self.dictionary.find_term(node.term_id).surface_form} ({node.start_index}-{node.end_index})\n"
            
        return string_representation
       
    def add_node(self, node: LatticeNode) -> None:
        node.term = self.dictionary.find_term(node.term_id)
        self.nodes.append(node)
        
        # Update the lattice length if need be
        if node.end_index > self.length:
            self.length = node.end_index
        
    def get_nodes_starting_at(self, index: int) -> filter:
        """
        Returns all nodes in the lattice with the requested start index
        :param index: The requested start index 
        :return: An iterable with all matching nodes
        """
        return filter(lambda node: node.start_index == index, self.nodes)
    
    def get_nodes_ending_at(self, index: int) -> filter:
        """
        Returns all nodes in the lattice with the requested end index
        :param index: The requested end index
        :return: An iterable with all matching nodes
        """
        return filter(lambda node: node.end_index == index, self.nodes)
        
    def find_optimal_path(self) -> List[LatticeNode]:
        """
        Find the minimal cost path through the lattice by running Viterbi's algorithm.
        :return: A list containing all nodes making up the path
        """
        # Add EOS node
        eos_node = LatticeNode(self.length, self.length + 1, 0, node_type=NodeType.EOS)
        self.add_node(eos_node)
        
        for i in range(0, self.length):
            current_node: LatticeNode
            for current_node in self.get_nodes_starting_at(i):
                previous_node: LatticeNode
                for previous_node in self.get_nodes_ending_at(i):
                    current_node_term: TermDictionaryEntry = self.dictionary.find_term(current_node.term_id)
                    previous_node_term: TermDictionaryEntry = self.dictionary.find_term(previous_node.term_id)
                    
                    current_node_cost: int = current_node_term.cost if current_node.node_type == NodeType.TERM else 0
                    connection_cost: int = self.dictionary.connection_costs.get_connection_cost(
                        current_node_term.left_context_id, 
                        previous_node_term.right_context_id) if current_node.node_type == NodeType.TERM else 0

                    previous_node_total_cost: int = previous_node.total_cost or previous_node_term.cost
                    current_node_total_cost: int = current_node_cost + connection_cost + previous_node_total_cost
                    
                    if current_node.total_cost is None or current_node_total_cost < current_node.total_cost :
                        current_node.total_cost = current_node_total_cost
                        current_node.previous_node = previous_node
                        
        # The optimal path can be traced back from recursively checking every node's "previous_node" 
        # from the end of the lattice
        optimal_path: List[LatticeNode] = []
        current_node: LatticeNode = next(self.get_nodes_ending_at(self.length))
        while current_node is not None:
            optimal_path.append(current_node)
            current_node = current_node.previous_node
        
        optimal_path.reverse()
        
        return optimal_path