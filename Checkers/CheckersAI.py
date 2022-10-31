import random

piece_score = {"k": 3, "m": 1, "-": 0}


def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]


# Find the best move based on material alone.
# it looks two moves ahead by using brute force
def find_best_move_brute_force(gs):
    turn_multiplier = 1 if gs.white_to_move else -1
    opponent_min_max_score = 100
    best_player_move = None
    possible_moves_extended = gs.get_all_possible_moves()
    # random.shuffle(possible_moves_extended) # to select random move among moves with same scores
    for player_move in possible_moves_extended:
        gs.make_move_extended(player_move)
        oppenent_moves = gs.get_all_possible_moves()
        opponent_max_score = -100
        for oppenent_move in oppenent_moves:
            gs.make_move_extended(oppenent_move)
            score = - turn_multiplier * score_material(gs.board)
            if score > opponent_max_score:
                opponent_max_score = score
            gs.undo_move()
        if opponent_max_score < opponent_min_max_score:
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move
        gs.undo_move()

    return best_player_move





# Score the board base on material
def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]

    return score


