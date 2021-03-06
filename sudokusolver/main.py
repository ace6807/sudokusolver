import itertools
from dataclasses import dataclass
from typing import Optional


@dataclass
class BoardPosition:
    row: int
    column: int


class SudokuBoard:
    def __init__(self, board: list) -> None:
        self.board = board
    
    def get_value(self, position: BoardPosition) -> int:
        return self.board[position.row][position.column]

    def get_row(self, position: BoardPosition) -> list:
        return self.board[position.row]

    def get_column(self, position: BoardPosition) -> list:
        return [row[position.column] for row in self.board]

    def is_complete(self) -> bool:
        for row in self.board:
            if 0 in row:
                return False
        return True

    def __str__(self) -> str:
        board_str = ""
        for row in self.board:
            board_str += "  — "*9 + "\n"
            for column in row:
                board_str += f'| {column} '
            board_str += "|\n"
        board_str += "  — "*9 + "\n"
        return board_str

    def __repr__(self) -> str:
        return self.__str__()


class SudokuSolver:
    @staticmethod
    def get_containing_small_square(position: BoardPosition):
        def get_index_group(index):
            index = index + 1
            if index % 3 == 0:
                return [index-3, index-2, index-1]
            if (index + 1) % 3 == 0:
                return [index-2, index-1, index]
            else:
                return [index-1, index, index + 1]

        row_index_group = get_index_group(position.row)
        column_index_group = get_index_group(position.column)

        return (BoardPosition(cell[0], cell[1]) for cell in itertools.product(row_index_group, column_index_group))

    @classmethod
    def check_valid_for_small_square(cls, board: SudokuBoard, positon: BoardPosition, value:int = None) -> bool:
        if not value:
            value = board.get_value(positon)
        for cell in cls.get_containing_small_square(positon):
            if cell != positon and board.get_value(cell) == value:
                return False
        return True

    @staticmethod
    def check_valid_for_direction(board: SudokuBoard, position: BoardPosition, direction_function, value: int=None):
        if not value:
            value = board.get_value(position)

        if value == board.get_value(position):
            expected_count = 1
        else:
            expected_count = 0

        return direction_function(position).count(value) == expected_count

    @classmethod
    def check_valid_for_row(cls, board: SudokuBoard, position: BoardPosition, value: int=None):
        return cls.check_valid_for_direction(board, position, board.get_row, value)

    @classmethod
    def check_valid_for_column(cls, board: SudokuBoard, position: BoardPosition, value: int=None):
        return cls.check_valid_for_direction(board, position, board.get_column, value)

    @classmethod
    def get_possible_values(cls, board: SudokuBoard, position: BoardPosition):
        return (
            i for i in range(1,10)
            if cls.check_valid_for_column(board, position, i) 
            and cls.check_valid_for_row(board, position, i) 
            and cls.check_valid_for_small_square(board, position, i)
        )

    @classmethod
    def get_next_empty_position(cls, board: SudokuBoard) -> Optional[BoardPosition]:
        for row_index, row in enumerate(board.board):
            for column_index, column in enumerate(board.board):
                next_position = BoardPosition(row_index, column_index)
                if not board.get_value(next_position):
                    return next_position

    @classmethod
    def solve(cls, board: SudokuBoard) -> bool:
        if board.is_complete():
            return True
        
        next_position = cls.get_next_empty_position(board)
        possible_values = cls.get_possible_values(board, next_position)

        for possible_value in possible_values:
            board.board[next_position.row][next_position.column] = possible_value
        
            if cls.solve(board):
                return True

            board.board[next_position.row][next_position.column] = 0
        return False    


board = SudokuBoard([
    [6,8,0,0,0,4,0,0,0],
    [1,0,4,0,0,0,0,8,9],
    [0,0,0,5,0,0,6,0,0],
    [0,0,9,0,7,5,0,0,0],
    [2,1,5,0,6,3,4,0,8],
    [8,7,0,0,4,2,9,5,3],
    [0,2,0,4,0,0,0,6,5],
    [0,0,0,2,0,9,8,0,7],
    [0,0,1,0,0,8,0,0,0],
])
