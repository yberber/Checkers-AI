"""
This is out main driver file/ It will be responsible for handling
user input and displaying the current GameState object.
"""
import math

import pygame
from Checkers import CheckersEngine, CheckersAI


BOARD_WIDTH = BOARD_HEIGHT = 640
MOVE_LOG_PANEL_WIDTH = 260
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 10  # dimensions of a checkers board are 10x10
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


# Initialize a global dictionary of images. This will be called exactly once in main
# Note: images will be changed with better ones later
def load_images():
    pieces = ["wm", "wk", "bm", "bk"]
    for piece in pieces:
        image = pygame.image.load("images/" + piece + "_.png")
        rect = image.get_rect()
        rect = rect.fit([0, 0, SQ_SIZE, SQ_SIZE])
        surface = pygame.Surface((SQ_SIZE, SQ_SIZE))
        surface.set_alpha(255)
        surface.blit(pygame.transform.scale(image, rect.size), rect)
        IMAGES[piece] = surface
        # IMAGES[piece] = pygame.transform.scale(image, (SQ_SIZE, (image.get_height() / image.get_width()) * SQ_SIZE))

    #  Note: we can access an image by saying 'IMAGES['wp']'


# The main driver for our code. This will handle user input and update the graphics
def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = pygame.time.Clock()
    screen.fill((255, 255, 255))
    move_log_font = pygame.font.SysFont("Arial", 12, False, False)
    gs = CheckersEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    load_images()  # only do this once, before the while loop
    running = True
    sq_selected = ()  # no square is selected, keep track of the last click of the used (tuple: (row, col))
    player_clicks = []  # keep track of player clicks (two tuples: [(6, 4), (5, 3)])
    possible_moves_for_selected = []
    player_one = True  # if a human is playing white, then this will be True. If an AI is playing, then False
    player_two = True  # Same as above but for black
    game_over = False
    paused = True  # can be used to pause the game while playing AI. User can press enter to pause the game
    while running:
        is_human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            # mouse handler
            elif e.type == pygame.MOUSEBUTTONDOWN and is_human_turn and not game_over:
                location = pygame.mouse.get_pos()  # (x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col) or col >= 10:  # the user clicked the same square or user clicked mouse log
                    sq_selected = ()  # deselect
                    player_clicks = []  # clear player clicks
                    possible_moves_for_selected = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)  # append for both 1st and 2nd clicks
                if len(player_clicks) == 1:
                    possible_moves_for_selected = gs.get_valid_moves_for_selected_piece(sq_selected)
                if len(player_clicks) == 2:  # after 2nd click
                    move = CheckersEngine.Move(player_clicks[0], player_clicks[1], gs.board, gs.white_to_move)
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
                    valid_moves = gs.get_valid_moves()
                    game_over = False
                if e.key == pygame.K_SPACE:
                    paused = not paused
                if e.key == pygame.K_r:  # reset the board when 'r' is pressed
                    gs = CheckersEngine.GameState()
                    player_clicks = []
                    sq_selected = ()
                    valid_moves = gs.get_valid_moves()
                    possible_moves_for_selected = []
                    game_over = False
                    move_made = False

        # AI Move Finder Logic
        if not is_human_turn and not game_over and not paused:
            ai_move = CheckersAI.find_best_move_min_max(gs, 5)

            if ai_move is None:
                ai_move = CheckersAI.find_random_move(valid_moves)

            # gs.make_move_extended(ai_move)
            if type(ai_move) is list:
                is_more_than_one_piece_captured = False
                for index in range(0, len(ai_move)-1):
                    gs.make_move(ai_move[index], seaching_mode=True)
                    animate_move(gs.move_log[-1], screen, gs.board, clock)
                    draw_game_state(screen, gs, possible_moves_for_selected, sq_selected, move_log_font)
                    pygame.display.flip()
                    is_more_than_one_piece_captured = True
                gs.make_move(ai_move[-1])
                if is_more_than_one_piece_captured:
                    gs.change_turn()
            else:
                gs.make_move(ai_move)

            move_made = True

        if move_made:
            animate_move(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.get_valid_moves()

            if is_human_turn and gs.capture_index >= 2:
                sq_selected = (gs.move_log[-1].end_row, gs.move_log[-1].end_col)
                player_clicks = [sq_selected]
                possible_moves_for_selected = gs.get_valid_moves_for_selected_piece(sq_selected)

            move_made = False
            if len(valid_moves) == 0:
                game_over = True
                draw_game_state(screen, gs, possible_moves_for_selected, sq_selected, move_log_font)
                if gs.white_to_move:
                    draw_end_game_text(screen, "Black Wins")
                else:
                    draw_end_game_text(screen, "White Wins")

        if not game_over:
            draw_game_state(screen, gs, possible_moves_for_selected, sq_selected, move_log_font)

        clock.tick(MAX_FPS)
        pygame.display.flip()


# Responsible for all the graphics within a current game state.
def draw_game_state(screen, gs, possible_moves, sq_selected, move_log_font):
    draw_board(screen)  # draw squares on the board
    highlight_squares(screen, gs, possible_moves, sq_selected)
    draw_pieces(screen, gs.board)  # draw pieces on top of those squares
    draw_move_log(screen, gs, move_log_font)


# Draw the squares on the board.
def draw_board(screen):
    global colors
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))



# Highlight square selected and moves for piece selected
def highlight_squares(screen, gs, possible_moves, sq_selected):
    if sq_selected != ():
        row, col = sq_selected
        if gs.board[row][col][0] == ("w" if gs.white_to_move else "b"):  # sq_selected is a piece that can be moved
            surface = pygame.Surface((SQ_SIZE, SQ_SIZE))
            surface.set_alpha(100)  # transparency value -> 0 0 transparent; 255 opaque
            # surface.fill(pygame.Color("blue"))
            surface.fill(pygame.Color("darkgreen"))
            screen.blit(surface, (col * SQ_SIZE, row * SQ_SIZE))
            # highlight moves from that square
            # surface.fill(pygame.Color("yellow"))
            surface = pygame.Surface((SQ_SIZE, SQ_SIZE))
            surface.set_alpha(100)  # transparency value -> 0 0 transparent; 255 opaque
            for move in possible_moves:
                pygame.draw.circle(surface, pygame.Color("darkgreen"), (SQ_SIZE//2,
                                                                       SQ_SIZE//2), SQ_SIZE/8)
                screen.blit(surface, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))


# Draw the pieces on the board using the current GameState.board
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# Draw the move log
def draw_move_log(screen, gs, font):
    pass
    move_log_rect = pygame.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    pygame.draw.rect(screen, pygame.Color("black"), move_log_rect)

    move_log = gs.move_log
    move_texts = []

    move_sequence_number = 1
    is_white_move = True
    move_string = ""
    for i in range(len(move_log)):
        move = move_log[i]
        if is_white_move == move.is_white and is_white_move:
            move_texts.append(move_string)
            move_string = str(move_sequence_number)
            move_sequence_number += 1

        move = move_log[i]

        if is_white_move == move.is_white:
            move_string += "     " + move.get_checkers_col_row_notation()

        else:
            move_string += move.get_notation_while_capturing()


        is_white_move = not move.is_white

    if move_string != "":
        move_texts.append(move_string)

    # print(len(move_log))
    padding_x = padding_y = 5
    y_pos = padding_y
    new_line_increment_y_by = 20

    adjust_text_starting_index = max(1, (len(move_texts) - MOVE_LOG_PANEL_HEIGHT // (padding_y + new_line_increment_y_by)  ))

    for i in range(adjust_text_starting_index, len(move_texts)):
        log_text = font.render(move_texts[i], True, pygame.Color("white"))
        screen.blit(log_text, (BOARD_WIDTH + padding_x, y_pos))
        y_pos += new_line_increment_y_by



# animating a move
def animate_move(move, screen, board, clock):
    global colors
    d_r = move.end_row - move.start_row
    d_c = move.end_col - move.start_col
    frames_per_square = 8  # frames to move one square
    frame_count = int(math.sqrt(d_r*d_r + d_c*d_c) * frames_per_square)
    for frame in range(frame_count + 1):
        d_frame = frame/frame_count
        row, col = (move.start_row + d_r * d_frame, move.start_col + d_c * d_frame)
        draw_board(screen)
        draw_pieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = pygame.Rect(move.end_col*SQ_SIZE, move.end_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, end_square)
        if move.captured_piece != "--":
            captured_row, captured_col = move.captured_piece_pos
            screen.blit(IMAGES[move.captured_piece], [captured_col * SQ_SIZE, captured_row * SQ_SIZE, SQ_SIZE, SQ_SIZE])
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)

def draw_end_game_text(screen, text):
    font = pygame.font.SysFont("Arial", 32, True, False)
    text_obj = font.render(text, True, pygame.Color("Gray"))
    text_location = pygame.Rect((BOARD_WIDTH - text_obj.get_width()) // 2, (BOARD_HEIGHT - text_obj.get_height()) // 2,
                                text_obj.get_width(), text_obj.get_height())
    screen.blit(text_obj, text_location)
    text_obj = font.render(text, True, pygame.Color("Black"))
    screen.blit(text_obj, text_location.move(2, 2))
    pygame.display.update()


# main function is going to run if CheckersMain is run.
# This notation prevent that function from running if this Python File is called by another file
if __name__ == '__main__':
    main()
