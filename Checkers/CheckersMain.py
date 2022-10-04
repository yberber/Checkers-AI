"""
This is out main driver file/ It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
from Checkers import CheckersEngine

WIDTH = HEIGHT = 640
DIMENSION = 10  # dimensions of a checkers board are 10x10
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


# Initialize a global dictionary of images. This will be called exactly once in main
# Note: images will be changed with better ones later
def load_images():
    pieces = ["wp", "wk", "bp", "bk"]
    for piece in pieces:
        image = p.image.load("images/" + piece + ".png")
        IMAGES[piece] = p.transform.scale(image, (SQ_SIZE, SQ_SIZE))
    #  Note: we can access an image by saying 'IMAGES['wp']'


# The main driver for our code. This will handle user input and update the graphics
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill((255, 255, 255))
    gs = CheckersEngine.GameState()
    print(gs.board)
    load_images()  # only do this once, before the while loop
    running = True
    sqSelected = ()  # no square is selected, keep track of the last click of the used (tuple: (row, col))
    playerClicks = []  # keep track of player clicks (two tuples: [(6, 4), (5, 3)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # the user clicked the same square
                    sqSelected = ()  # deselect
                    playerClicks = []  # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks
                if len(playerClicks) == 2:  # after 2nd click
                    move = CheckersEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.get_checkers_notation())
                    gs.make_move(move)
                    sqSelected = ()  # reset user clicks
                    playerClicks = []

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


# Responsible for all the graphics within a current game state.
def draw_game_state(screen, gs):
    draw_board(screen)  # draw squares on the board
    # add in piece highlighting or move suggestions (later)
    draw_pieces(screen, gs.board)  # draw pieces on top of those squares


# Draw the squares on the board.
def draw_board(screen):
    for y in range(10):
        for x in range(10):
            colors = [p.Color("white"), p.Color("gray")]
            for row in range(DIMENSION):
                for col in range(DIMENSION):
                    color = colors[(row + col) % 2]
                    p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# Draw the pieces on the board using the current GameState.board
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# main function is going to run if CheckersMain is run.
# This notation prevent that function from running if this Python File is called by another file
if __name__ == '__main__':
    main()
