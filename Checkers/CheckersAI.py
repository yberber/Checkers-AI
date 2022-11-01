import random

piece_score = {"k": 3, "m": 1, "-": 0}
DEPTH = 0
counter = 0


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


# Helper method to make first recursive call
def find_best_move_min_max(gs, depth=8):
    global next_move, DEPTH, counter
    counter = 0
    next_move = None
    DEPTH = depth
    # find_move_min_max(gs, depth)
    find_move_min_max_alpha_beta(gs, depth, -100, 100)
    # find_move_nega_max(gs, depth, 1 if gs.white_to_move else -1)
    print(f"possible move count: {counter}")
    return next_move

def find_move_min_max(gs, depth):
    global next_move
    global counter

    counter += 1

    if depth == 0:
        return score_material(gs.board)

    if gs.white_to_move:
        max_score = -100
        possible_moves_extended = gs.get_all_possible_moves()
        # if depth == DEPTH:
        #     random.shuffle(possible_moves_extended)
        for move in possible_moves_extended:
            gs.make_move_extended(move)
            score = find_move_min_max(gs, depth-1)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return max_score
    else:
        min_score = 100
        possible_moves_extended = gs.get_all_possible_moves()

        for move in possible_moves_extended:
            gs.make_move_extended(move)
            score = find_move_min_max(gs, depth - 1)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score

def find_move_min_max_alpha_beta(gs, depth, alpha, beta):
    global next_move
    global counter

    counter += 1

    if depth == 0:
        return score_material(gs.board)

    if gs.white_to_move:
        max_score = -100
        possible_moves_extended = gs.get_all_possible_moves()
        # if depth == DEPTH:
        #     random.shuffle(possible_moves_extended)
        for move in possible_moves_extended:
            gs.make_move_extended(move)
            score = find_move_min_max_alpha_beta(gs, depth-1, alpha, beta)

            if score > max_score:
                max_score = score
                if max_score >= beta:
                    gs.undo_move()
                    break
                if depth == DEPTH:
                    next_move = move
            alpha = max(alpha, max_score)
            gs.undo_move()
        return max_score
    else:
        min_score = 100
        possible_moves_extended = gs.get_all_possible_moves()
        # if depth == DEPTH:
        #     random.shuffle(possible_moves_extended)
        for move in possible_moves_extended:
            gs.make_move_extended(move)
            score = find_move_min_max_alpha_beta(gs, depth - 1, alpha, beta)
            if score < min_score:
                min_score = score
                if min_score <= alpha:
                    gs.undo_move()

                    break
                if depth == DEPTH:
                    next_move = move
            beta = min(beta, min_score)
            gs.undo_move()
        return min_score

def find_best_move_nega_max(gs, depth=8):
    global next_move, DEPTH, counter
    counter = 0
    next_move = None
    DEPTH = depth
    # find_move_min_max(gs, depth)
    # find_move_nega_max(gs, depth, 1 if gs.white_to_move else -1)
    find_move_nega_max_alpha_beta(gs, depth, -100, 100, 1 if gs.white_to_move else -1)

    print(f"possible move count: {counter}")
    return next_move

def find_move_nega_max(gs, depth, turn_multiplier):
    global next_move, counter
    counter += 1
    if depth == 0:
        return turn_multiplier * score_material(gs.board)

    max_score = -100
    possible_moves_extended = gs.get_all_possible_moves()
    for move in possible_moves_extended:
        gs.make_move_extended(move)
        score = -find_move_nega_max(gs, depth-1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
    return max_score


def find_move_nega_max_alpha_beta(gs, depth, alpha, beta, turn_multiplier):
    global next_move, counter
    counter += 1
    if depth == 0:
        return turn_multiplier * score_material(gs.board)

    # move ordering - implement later
    max_score = -100
    possible_moves_extended = gs.get_all_possible_moves()
    for move in possible_moves_extended:
        gs.make_move_extended(move)
        score = -find_move_nega_max_alpha_beta(gs, depth-1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
        if max_score > alpha:  # pruning happens
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


# a positive score is good for white, a negative score is good for black
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


