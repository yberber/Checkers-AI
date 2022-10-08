"""
This is out main driver file/ It will be responsible for handling
user input and displaying the current GameState object.
"""

import pygame
from Checkers import CheckersEngine

WIDTH = HEIGHT = 640
DIMENSION = 10  # dimensions of a checkers board are 10x10
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


# Initialize a global dictionary of images. This will be called exactly once in main
# Note: images will be changed with better ones later
def load_images():
    pieces = ["wm", "wk", "bm", "bk"]
    for piece in pieces:
        image = pygame.image.load("images/" + piece + ".png")
        IMAGES[piece] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))
    #  Note: we can access an image by saying 'IMAGES['wp']'


# The main driver for our code. This will handle user input and update the graphics
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill((255, 255, 255))
    gs = CheckersEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    load_images()  # only do this once, before the while loop
    running = True
    sq_selected = ()  # no square is selected, keep track of the last click of the used (tuple: (row, col))
    player_clicks = []  # keep track of player clicks (two tuples: [(6, 4), (5, 3)])
    possible_moves_for_selected = []
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            # mouse handler
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()  # (x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):  # the user clicked the same square
                    sq_selected = ()  # deselect
                    player_clicks = []  # clear player clicks
                    possible_moves_for_selected = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)  # append for both 1st and 2nd clicks
                if len(player_clicks) == 1:
                    possible_moves_for_selected = gs.get_valid_moves_for_selected_piece(sq_selected)
                if len(player_clicks) == 2:  # after 2nd click
                    move = CheckersEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    possible_moves_for_selected = []

                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            gs.make_move(valid_moves[i])
                            move_made = True
                            sq_selected = ()  # reset user clicks
                            player_clicks = []
                    if not move_made:
                        player_clicks = [sq_selected]
                        possible_moves_for_selected = gs.get_valid_moves_for_selected_piece(sq_selected)

            # key handle
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:  # undo when 'z' is pressed
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs, possible_moves_for_selected, sq_selected)
        clock.tick(MAX_FPS)
        pygame.display.flip()


# Responsible for all the graphics within a current game state.
def draw_game_state(screen, gs, possible_moves, sq_selected):
    draw_board(screen)  # draw squares on the board
    highlight_squares(screen, gs, possible_moves, sq_selected)
    draw_pieces(screen, gs.board)  # draw pieces on top of those squares


# Highlight square selected and moves for piece selected
def highlight_squares(screen, gs, possible_moves, sq_selected):
    if sq_selected != ():
        row, col = sq_selected
        if gs.board[row][col][0] == ("w" if gs.white_to_move else "b"):  # sq_selected is a piece that can be moved
            surface = pygame.Surface((SQ_SIZE, SQ_SIZE))
            surface.set_alpha(100)  # transparency value -> 0 0 transparent; 255 opaque
            surface.fill(pygame.Color("blue"))
            screen.blit(surface, (col * SQ_SIZE, row * SQ_SIZE))
            # highlight moves from that square
            surface.fill(pygame.Color("yellow"))
            for move in possible_moves:
                screen.blit(surface, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))


# Draw the squares on the board.
def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# Draw the pieces on the board using the current GameState.board
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# main function is going to run if CheckersMain is run.
# This notation prevent that function from running if this Python File is called by another file
if __name__ == '__main__':
    main()
