
import pygame
from config import GameConfig, Colours
from typing import Optional
from game_rules import GameRules
from checkers_board import CheckerBoard
from pieces import Piece


WIN = pygame.display.set_mode((GameConfig.WIDTH, GameConfig.HEIGHT))
pygame.display.set_caption("Checkers")

BACKGROUND = pygame.Rect(0, 0, GameConfig.WIDTH, GameConfig.HEIGHT)

CheckerBoard.create_all_boxes()

all_square = CheckerBoard.all_board_bits
all_piece = Piece.initiate_pieces()

def capture(piece: Piece):
    #square: Optional[CheckerBoard] = None
    for sqr in all_square:
        if sqr.contains_piece is piece:
            sqr.contains_piece = None

    piece.coord = (0, 0)
    all_piece.remove(piece)

def set_piece_coords_and_colour(piece_list, all_squares) -> None:
    for piece in piece_list:
        set_piece_colour(piece)
        for square in all_squares:
            if square.column == piece.col_row[0] and square.row == piece.col_row[1]:
                piece.coord = square.center

def set_piece_colour(piece: Piece):
    if piece.is_white == True:
        piece.colour = Colours.WHITE_PIECE
    else:
        piece.colour = Colours.BLACK_PIECE


def get_selected_piece():
    for i in all_piece:
        if i.is_selected == True:
            return i

def draw_squares(all_square):
    for piece in all_square:
        rect = pygame.Rect(piece.x, piece.y, piece.side_length, piece.side_length)

        colour = 0
        if piece.colour == 0:
            colour = Colours.WHITE
        else:
            colour = Colours.BLACK

        pygame.draw.rect(WIN, colour, rect)

def process_click(click_location: tuple[int, int]):
    return CheckerBoard.find_clicked_box(click_location)

def select_piece(piece: Piece) -> bool:
    if GameRules.whites_turn == piece.is_white:
        piece.is_selected = True
        piece.colour = Colours.SELECTED_COLOUR
        #GameRules.whites_turn = not GameRules.whites_turn
        return True
    else:
        return False


def unselect_piece():
    piece = get_selected_piece()
    piece.is_selected = False
    if piece.is_white == True:
        piece.colour = Colours.WHITE_PIECE
    else:
        piece.colour = Colours.BLACK_PIECE

def move_piece(box: CheckerBoard):
    selected_piece: Optional[Piece] = None
    for i in all_piece:
        if i.is_selected == True:
            selected_piece = i
    if box.contains_piece is None:
        box.contains_piece = selected_piece
        if selected_piece is not None:
            selected_piece.change_position(box)
            if GameRules.whites_turn == selected_piece.is_white:
                GameRules.whites_turn = not GameRules.whites_turn

            Piece.check_to_crown(selected_piece)
        return True
    else:
        return False



def draw():
    pygame.draw.rect(WIN, Colours.BACKGROUND_COLOUR, BACKGROUND)
    draw_squares(all_square)
    
    for piece in all_piece:
        if piece.is_dead is False:
            pygame.draw.circle(WIN, piece.colour, piece.coord, piece.radius)
            if piece.is_crown and piece.is_white:
                pygame.draw.circle(WIN, piece.white_crown_colour, piece.coord, piece.crown_radius)
            elif piece.is_crown and not piece.is_white:
                pygame.draw.circle(WIN, piece.black_crown_colour, piece.coord, piece.crown_radius)



    pygame.display.update()

def main():
    clock = pygame.time.Clock()


    piece_selected: bool = False
    run: bool = True
    set_piece_coords_and_colour(all_piece, all_square)
    while run:
        clock.tick(GameConfig.FPS)
        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_location = pygame.mouse.get_pos()
                box = process_click(click_location)
                piece = None
                valid_box_to_move: bool = False
                if box != None:
                    piece = box.contains_piece

                if piece_selected:
                    valid_box_to_move = GameRules.check_valid_square_to_move(get_selected_piece(), box)

                if not piece_selected and piece != None: 
                    if select_piece(piece):
                        piece_selected = True          
                    
                elif piece_selected and box == None:
                    piece_selected = False
                    unselect_piece()
                elif piece_selected and box != None:
                    piece_selected = False
                    if valid_box_to_move is True:
                        move_piece(box)
                    elif isinstance(valid_box_to_move, Piece):
                        if move_piece(box):
                            capture(valid_box_to_move)
                    unselect_piece()

    pygame.quit()


main()