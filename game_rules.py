from typing import List, Tuple, Optional
from pieces import Piece
from checkers_board import CheckerBoard

class GameRules:
    whites_turn: bool = True

    @staticmethod
    def finder(num: int, possible_num: list[int]):
        if num == 1:
            possible_num.append(num)
            possible_num.append(num+1)
        elif num == 8:
            possible_num.append(num-1)
            possible_num.append(num)
        else:
            possible_num.append(num-1)
            possible_num.append(num)
            possible_num.append(num+1)
    
    @staticmethod
    def get_valid_square_to_move(piece: Piece) -> List[Tuple[CheckerBoard, Optional[Piece]]]:
        current_square: CheckerBoard = piece.get_square()
        col: int = current_square.column
        row: int = current_square.row


        possible_cols: list[int] = []
        possible_rows: list[int] = []

        valid_col_row: list[tuple[int, int]] = []

        GameRules.finder(col, possible_cols)
        GameRules.finder(row, possible_rows)

        for i in possible_cols:
            for j in possible_rows:
                if (i+j)%2==1:
                    valid_col_row.append((i, j))
        
        valid_col_row.remove((col, row))

        backwards_move: List[Tuple[int, int]] = []
        if piece.is_crown is False:
            for col_row in valid_col_row:
                if col_row[1] <= piece.col_row[1] and piece.is_white is False:
                    backwards_move.append(col_row)
                elif col_row[1] >= piece.col_row[1] and piece.is_white is True:
                    backwards_move.append(col_row)
            
            for (i, j) in backwards_move:
                valid_col_row.remove((i, j))

        valid_squares: List[Tuple[CheckerBoard, Optional[Piece]]] = []

        for col_row in valid_col_row:
            square: CheckerBoard = CheckerBoard.get_box_by_col_row(col_row)
            if square.contains_piece is None:
                valid_squares.append((CheckerBoard.get_box_by_col_row(col_row), None))
            elif square.contains_piece is not None:
                jump_square_coord = current_square.jump_over(square)
                if jump_square_coord is not None:
                    valid_squares.append((CheckerBoard.get_box_by_col_row(jump_square_coord), square.contains_piece))
        
        return valid_squares


    @classmethod
    def check_valid_square_to_move(cls, piece: Piece, new_square: CheckerBoard):
        for square in cls.get_valid_square_to_move(piece):
            if new_square == square[0] and square[1] is not None:
                return square[1]
            elif new_square == square[0] and square[1] is None:
                return True
        else:
            return False