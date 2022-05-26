import pygame
from game_rules import GameRules
from checkers_board import CheckerBoard
from pieces import Piece

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SELECTED_COLOUR = (255, 0, 0)
BACKGROUND_COLOUR = (103, 20, 13)

BLACK_PIECE = (103, 68, 10)
WHITE_PIECE = (221, 176, 99)

BACKGROUND = pygame.Rect(0, 0, WIDTH, HEIGHT)

CheckerBoard.create_all_boxes()

all_square = CheckerBoard.all_board_bits
all_piece = Piece.initiate_pieces()

def capture(piece: Piece):
    all_piece.remove(piece)

def set_piece_coords_and_colour(piece_list, all_squares) -> None:
    for piece in piece_list:
        set_piece_colour(piece)
        for square in all_squares:
            if square.column == piece.col_row[0] and square.row == piece.col_row[1]:
                piece.coord = square.center

def set_piece_colour(piece: Piece):
    if piece.is_white == True:
        piece.colour = WHITE_PIECE
    else:
        piece.colour = BLACK_PIECE


def get_selected_piece():
    for i in all_piece:
        if i.is_selected == True:
            return i

def draw_squares(all_square):
    for piece in all_square:
        rect = pygame.Rect(piece.x, piece.y, piece.side_length, piece.side_length)

        colour = 0
        if piece.colour == 0:
            colour = WHITE
        else:
            colour = BLACK

        pygame.draw.rect(WIN, colour, rect)

def process_click(click_location: tuple[int]):
    return CheckerBoard.find_clicked_box(click_location)

def select_piece(piece: Piece) -> bool:
    if GameRules.whites_turn == piece.is_white:
        piece.is_selected = True
        piece.colour = SELECTED_COLOUR
        #GameRules.whites_turn = not GameRules.whites_turn
        return True
    else:
        return False


def unselect_piece():
    piece = get_selected_piece()
    piece.is_selected = False
    if piece.is_white == True:
        piece.colour = WHITE_PIECE
    else:
        piece.colour = BLACK_PIECE

def move_piece(box: CheckerBoard):
    selected_piece: Piece = None
    for i in all_piece:
        if i.is_selected == True:
            selected_piece = i

    box.contains_piece = selected_piece
    selected_piece.change_position(box)

    if GameRules.whites_turn == selected_piece.is_white:
        GameRules.whites_turn = not GameRules.whites_turn



def draw():
    pygame.draw.rect(WIN, BACKGROUND_COLOUR, BACKGROUND)
    draw_squares(all_square)
    
    for piece in all_piece:
        if piece.is_dead is False:
            pygame.draw.circle(WIN, piece.colour, piece.coord, piece.radius)


    pygame.display.update()

def main():
    clock = pygame.time.Clock()


    piece_selected = False
    run = True
    set_piece_coords_and_colour(all_piece, all_square)
    while run:
        clock.tick(FPS)
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
                        move_piece(box)
                        capture(valid_box_to_move)
                    unselect_piece()

    pygame.quit()


main()