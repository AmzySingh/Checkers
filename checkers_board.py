
from typing import Generic, List, Any, ClassVar, TypeVar



class CheckerBoard:
    #CheckerBoard = TypeVar('CheckerBoard')
    starting_position: ClassVar[tuple[int, int]] = (100, 100)
    box_length: ClassVar[int] = 100
    all_board_bits: ClassVar[List[Any]] = []

    def __init__(self, column: int, row: int, contains_piece):
        self.column = column
        self.row = row
        self.contains_piece = contains_piece
        self.side_length = self.box_length
        self.x = self.starting_position[0] + (self.column - 1)*self.box_length
        self.y = self.starting_position[1] + (self.row - 1)*self.box_length
        self.colour = (self.row + self.column)%2
        self.center = (self.x + self.side_length/2, self.y + self.side_length/2)
    
    @classmethod
    def find_clicked_box(cls, coords: tuple[int, int]) :
        for square in cls.all_board_bits:
            if coords[0] >= square.x and coords[0] < (square.x + square.side_length) and coords[1] >= square.y and coords[1] < (square.y + square.side_length):
                return square
        else:
            return None

    @classmethod
    def get_box_by_col_row(cls, col_row: tuple[int, int]):
        for square in CheckerBoard.all_board_bits:
            col, row = col_row
            if square.column == col and square.row == row:
                return square



    @classmethod
    def create_all_boxes(cls):
        for column in range(1, 9):
            for row in range(1, 9):
                piece = cls(column, row, None)
                cls.all_board_bits.append(piece)


    def jump_over(self, other):
        col_change = self.column - other.column
        row_change = self.row - other.row

        new_locations = (other.column - col_change, other.row - row_change)
        not_allowed = [0, 9]
        if new_locations[0] in not_allowed and new_locations[1] in not_allowed:
            return None
        else:
            return new_locations


    def __repr__(self) -> str:
        return f'({self.column}, {self.row})'



