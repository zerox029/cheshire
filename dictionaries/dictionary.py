from typing import KeysView, Any

from pygtrie import CharTrie
from dictionaries.connection_matrix import ConnectionMatrix
from dictionaries.term_dictionary import TermDictionary, TermDictionaryEntry


class Dictionary:
    """
    A metaclass storing information from two data sources. A term dictionary, stored in list and trie form
    as well as a connection matrix containing connection cost information.
    Not to be confused with the term dictionary.
    """
    def __init__(self, terms: TermDictionary, connection_costs: ConnectionMatrix):
        self.terms: TermDictionary = terms
        self.terms_trie: CharTrie = self.__init_trie() 
        self.connection_costs: ConnectionMatrix = connection_costs
        
    def __init_trie(self) -> CharTrie:
        """
        Generates a trie to efficiently store the term dictionary.
        This is required to avoid being bottle-necked by dictionary lookups in the segmenting process
        :return: The generated trie
        """
        terms_trie: CharTrie = CharTrie()
        for i, term in self.terms.enumerate_terms():
            terms_trie[term.surface_form] = i

        return terms_trie
        
    def common_prefix_search(self, input_string: str) -> KeysView[Any]:
        """"
        Find all words in the dictionary that share a common prefix given an input string.
        東京に住む would return 東 and 東京 for example.
        """
        return self.terms_trie.prefixes(input_string)
    
    def find_term(self, term_id: int) -> TermDictionaryEntry:
        """
        Get a term dictionary entry corresponding to a given term id.
        :param term_id: The requested term id
        :return: The associated term dictionary entry
        """
        return self.terms.get_term(term_id) 