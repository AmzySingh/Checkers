from checkers_board import CheckerBoard
from typing import List

class Piece:
    def __init__(self, col_row, is_white):
        self.col_row = col_row
        self.coord = (0, 0)
        self.is_white = is_white
        self.colour = None
        self.is_crown = False
        self.radius = 40
        self.is_selected = False
        self.is_dead = False

    def add_to_square(self):
        for square in CheckerBoard.all_board_bits:
            if square.column == self.col_row[0] and square.row == self.col_row[1]:
                square.contains_piece = self

    def change_position(self, box: CheckerBoard):
        for square in CheckerBoard.all_board_bits:
            if square.contains_piece == self:
                square.contains_piece = None
        self.col_row = (box.column, box.row)
        self.coord = box.center
        box.contains_piece = self


    def get_square(self):
        for square in CheckerBoard.all_board_bits:
            if self == square.contains_piece:
                return square

    def check_to_crown(self):
        if self.is_white == True and self.col_row[1] == 1:
            self.is_crown = True
        elif self.is_white == False and self.col_row[1] == 8:
            self.is_crown = True
        

    @classmethod
    def initiate_pieces(cls):
        all_pieces: List[Piece] = []

        for i in range(1, 9):
            for j in range(6, 9):
                if (i+j)%2 == 1:
                    piece = cls((i, j), True)
                    all_pieces.append(piece)
                    piece.add_to_square()

        for i in range(1, 9):
            for j in range(1, 4):
                if (i+j)%2 == 1:
                    piece = cls((i, j), False)
                    all_pieces.append(piece)
                    piece.add_to_square()

        return all_pieces



    def __repr__(self) -> str:
        return f'col_row: {self.col_row}'








        