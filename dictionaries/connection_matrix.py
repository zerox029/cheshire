import csv
from typing import List

from typing_extensions import Self

class ConnectionMatrix:
    """
    A connection cost matrix
    """
    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix
    
    @staticmethod
    def from_file(file_name: str, encoding: str = "utf-8") -> Self:
        """
        Generates a connection cost matrix from a given file.
        The input file should follow the ipadic format.
        :param file_name: The relative path of the csv file
        :param encoding: The encoding of the csv file (defaults to UTF-8)
        :return: The created connection matrix
        """
        with open(file_name, "r", encoding=encoding) as dict:
            dict_reader = csv.reader(dict, delimiter=" ")
            size_line = next(dict_reader)
            matrix_size: (int, int) = (int(size_line[0]), int(size_line[1]))
            
            assert matrix_size[0] == matrix_size[1]

            connection_matrix: List[List[int]] = [[0] * matrix_size[0] for i in range(matrix_size[1])]
            
            for row in dict_reader:
                x, y, cost = int(row[0]), int(row[1]), int(row[2])
                connection_matrix[x][y] = cost
 
            return ConnectionMatrix(connection_matrix)
        
    def get_connection_cost(self, left_id: int, right_id: int) -> int:
        """
        Get the connection cost between two nodes.
        :param left_id: The left context id
        :param right_id: The right context id
        :return: The corresponding connection cost
        """
        return self.matrix[left_id][right_id]