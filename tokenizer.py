import glob
from typing import List

from dictionaries.connection_matrix import ConnectionMatrix
from dictionaries.dictionary import Dictionary
from dictionaries.term_dictionary import TermDictionary
from lattice import Lattice, LatticeNode


def main():
    tokenized = tokenize("お前はもう死んでいる")
    print(*tokenized, sep="\n")
    
def tokenize(input_string: str) -> List[LatticeNode]:
    dictionary = import_ipadic()
    lattice = Lattice(dictionary)
    
    
    for i in range(0, len(input_string)):
        # TODO: Skip the current iteration if the lattice contains no nodes ending at the previous index
        
        current_lookup_string: str = input_string[i:len(input_string)]        
        candidate_terms = dictionary.common_prefix_search(current_lookup_string) 
        
        for (term, term_id) in candidate_terms:
            dictionary_term = dictionary.find_term(term_id)
            term_length = len(dictionary_term.surface_form)
            node = LatticeNode(i, i + term_length, term_id)
            lattice.add_node(node)

    return lattice.find_optimal_path()

def import_ipadic() -> Dictionary:
    """
    Set up the in-memory dictionary from ipadic files.
    Due to the size of the dictionary, this operation is extremely costly 
    and should only be done once at the start. Subsequent lookups are extremely fast.
    :return: The generated dictionary
    """
    path: str = "resources/mecab-ipadic-2.7.0-20070801"
    extension: str = "csv"
    term_dictionary_files: List[str] = glob.glob(path + f'/*.{extension}')
    
    term_dictionary: TermDictionary = TermDictionary.from_files(term_dictionary_files)
    connection_matrix: ConnectionMatrix = ConnectionMatrix.from_file("resources/mecab-ipadic-2.7.0-20070801/matrix.def")

    return Dictionary(term_dictionary, connection_matrix)
        
if __name__ == '__main__':
    main()