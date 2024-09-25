import csv
from collections.abc import Iterable
from enum import Enum
from typing import List, Tuple
from typing_extensions import Self

class PartOfSpeech(Enum):
    """
    The specific part of speech of a term
    """
    NOUN: str = "名詞"
    ADJ: str = "形容詞"
    VERB: str = "動詞"
    AUX_VERB: str = "助動詞"
    PARTICLE: str = "助詞"
    PUNC: str = "記号"
    UNKNOWN: str = "不明"
    
    @staticmethod
    def from_str(label) -> Self:
        if label == "名詞":
            return PartOfSpeech.NOUN
        elif label == "形容詞":
            return PartOfSpeech.ADJ
        elif label == "動詞":
            return PartOfSpeech.VERB
        elif label == "助動詞":
            return PartOfSpeech.AUX_VERB
        elif label == "助詞":
            return PartOfSpeech.PARTICLE
        elif label == "記号":
            return PartOfSpeech.PUNC
        else:
            return PartOfSpeech.UNKNOWN

class Features:
    """
    The extra grammatical features included in a term dictionary entry
    """
    def __init__(self, part_of_speech: PartOfSpeech, subdivision: str):
        self.part_of_speech: PartOfSpeech = part_of_speech
        self.subdivision: str = subdivision
        
    def __str__(self) -> str:
        return f"{self.part_of_speech.value} {self.subdivision}"
        

class TermDictionaryEntry:
    """
    A single term dictionary entry
    """
    def __init__(self, surface_form: str, left_context_id: int, right_context_id: int, cost: int, features: Features):
        self.surface_form = surface_form
        self.left_context_id = left_context_id
        self.right_context_id = right_context_id
        self.cost = cost
        self.features = features
        
    def __str__(self) -> str:
        return f"{self.surface_form} {self.left_context_id} {self.right_context_id} {self.cost} {self.features}"

class TermDictionary:
    """
    A glorified list of terms. Not to confuse with the regular dictionary, 
    this only contains terms without their associated connection costs
    """
    def __init__(self, terms: List[TermDictionaryEntry]):
        self.terms: List[TermDictionaryEntry] = terms

    def __str__(self) -> str:
        return '\n'.join(str(term) for term in self.terms)
        
    @staticmethod
    def from_files(file_names: List[str], encoding: str = "EUC-JP") -> Self:
        """
        Generate a term dictionary from a given csv file
        :param file_names: The relative paths of the csv files to import
        :param encoding: The encoding of the csv file (defaults to EUC-JP)
        :return: The created term dictionary
        """
        terms: List[TermDictionaryEntry] = []
        for file_name in file_names:
            with open(file_name, "r", encoding=encoding) as dict:
                dict_reader = csv.reader(dict, delimiter=",")
                for term in dict_reader:
                    term_entry = TermDictionaryEntry(term[0], 
                                                     int(term[1]), 
                                                     int(term[2]), 
                                                     int(term[3]), 
                                                     Features(PartOfSpeech.from_str(term[4]), term[5]))
                    terms.append(term_entry)

        return TermDictionary(terms)
    
    def enumerate_terms(self) -> enumerate[TermDictionaryEntry]:
        """
        Enumerate all terms in the term dictionary
        :return: 
        """
        return enumerate(self.terms)
    
    def get_term(self, term_id: int) -> TermDictionaryEntry:
        """
        Get the term associated with a given term id
        :param term_id: The requested term id 
        :return: The associated term
        """
        return self.terms[term_id]