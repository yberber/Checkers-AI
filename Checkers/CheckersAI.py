import random
import time
import CheckersEngine

piece_score = {"k": 3, "m": 1, "-": 0}
DEPTH = 0
counter = 0
current_time = 0
next_move = None


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
        opponent_max_score = -255
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


# alpha = the worst possible score for white
# beta = the worst possible score gor black
def find_move_min_max_alpha_beta_improved(gs, depth, alpha, beta):
    global next_move
    global counter

    # if gs.is_game_over():
    #     print(f"GAME OVER works for {'white' if not gs.white_to_move else 'black'}")
    #     return 255 if not gs.white_to_move else -255

    if depth == 0:

        counter += 1
        possible_moves_extended = gs.get_all_possible_captures()
        if len(possible_moves_extended) > 0:
            depth += 1
        else:
            return score_material(gs.board)
    else:
        possible_moves_extended = gs.get_all_possible_moves()
        if len(possible_moves_extended) == 0:
            counter += 1

            print(f"GAME ENDS AND {'black' if gs.white_to_move else 'white'} wins. Depth: {depth}")
            return -100 if gs.white_to_move else 100

    # if depth == DEPTH:
    #     random.shuffle(possible_moves_extended)



    move_id = 0

    if depth == DEPTH and len(possible_moves_extended) == 1:
        counter += 1
        next_move = possible_moves_extended[0]
        return


    if gs.white_to_move:
        max_score = -255
        for move in possible_moves_extended:


            move_id += 1
            gs.make_move_extended(move)
            score = find_move_min_max_alpha_beta_improved(gs, depth - 1, alpha, beta)
            # print(f"Score: {score}, max_score: {max_score}, depth: {depth}, alpha: {alpha}, beta: {beta}")
            if score > max_score:
                max_score = score
                alpha = max(alpha, max_score)
                if alpha >= beta:
                    gs.undo_move()
                    break
                if depth == DEPTH:
                    next_move = move
                    print(f"turn: {'white'}, move_id: {move_id}, counter: {counter}, score: {score}, used time: {(time.time() - current_time)}")


            gs.undo_move()
        return max_score
    else:
        min_score = 255
        for move in possible_moves_extended:
            move_id += 1
            gs.make_move_extended(move)
            score = find_move_min_max_alpha_beta_improved(gs, depth - 1, alpha, beta)
            if score < min_score:
                min_score = score
                beta = min(beta, min_score)
                if beta <= alpha:
                    gs.undo_move()
                    break
                if depth == DEPTH:
                    next_move = move
                    print(f"turn: {'black'}, move_id: {move_id}, counter: {counter}, score: {score}, used time: {(time.time() - current_time)}")
                    if len(possible_moves_extended) == 1:
                        break
            gs.undo_move()
        return min_score


# Helper method to make first recursive call
def find_best_move_min_max(gs, depth=8):
    global next_move, DEPTH, counter, current_time
    counter = 0
    DEPTH = depth
    # find_move_min_max(gs, depth)
    next_move = None
    current_time = time.time()
    find_move_min_max_alpha_beta_improved(gs, depth, -255, 255)
    print(f"possible move count: {counter}, time: {time.time() - current_time}")
    print("*******************************")
    return next_move


def find_move_min_max_alpha_beta(gs, depth, alpha, beta):
    global next_move
    global counter

    if depth == 0:
        counter += 1
        return score_material(gs.board)

    possible_moves_extended = gs.get_all_possible_moves()

    # if depth == DEPTH:
    #     random.shuffle(possible_moves_extended)

    move_id = 0

    if gs.white_to_move:
        max_score = -255
        for move in possible_moves_extended:
            move_id += 1
            gs.make_move_extended(move)
            score = find_move_min_max_alpha_beta(gs, depth-1, alpha, beta)
            if score > max_score:
                max_score = score
                if max_score >= beta:
                    gs.undo_move()
                    break
                if depth == DEPTH:
                    next_move = move
                    print(f"move_id: {move_id}, counter: {counter}, score: {score}, used time: {(time.time() - current_time)}")

            alpha = max(alpha, max_score)
            gs.undo_move()
        return max_score
    else:
        min_score = 255
        for move in possible_moves_extended:
            move_id += 1
            gs.make_move_extended(move)
            score = find_move_min_max_alpha_beta(gs, depth - 1, alpha, beta)
            if score < min_score:
                min_score = score
                if min_score <= alpha:
                    gs.undo_move()
                    break
                if depth == DEPTH:
                    next_move = move
                    print(f"move_id: {move_id}, counter: {counter}, score: {score}, used time: {(time.time() - current_time)}")

            beta = min(beta, min_score)
            gs.undo_move()
        return min_score

def find_move_min_max(gs, depth):
    global next_move
    global counter

    counter += 1

    if depth == 0:
        return score_material(gs.board)

    possible_moves_extended = gs.get_all_possible_moves()

    # if depth == DEPTH:
    #     random.shuffle(possible_moves_extended)

    if gs.white_to_move:
        max_score = -255
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
        min_score = 255
        for move in possible_moves_extended:
            gs.make_move_extended(move)
            score = find_move_min_max(gs, depth - 1)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score




def find_best_move_nega_max(gs, depth=8):
    global next_move, DEPTH, counter, current_time
    counter = 0
    next_move = None
    DEPTH = depth
    # find_move_nega_max(gs, depth, 1 if gs.white_to_move else -1)
    current_time = time.time()
    find_move_nega_max_alpha_beta(gs, depth, -255, 255, 1 if gs.white_to_move else -1)

    print(f"possible move count: {counter}, used time: {(time.time() - current_time)}")
    return next_move


def find_move_nega_max(gs, depth, turn_multiplier):
    global next_move, counter
    counter += 1

    if depth == 0:
        return turn_multiplier * score_material(gs.board)

    possible_moves_extended = gs.get_all_possible_moves()

    max_score = -255

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
    # counter += 1

    if depth == 0:
        counter += 1

        # possible_moves_extended = gs.get_all_possible_moves()
        # if len(possible_moves_extended) == 0:
        #     return -255
        # if gs.is_capturing:
        #     depth = 1
        # else:
        #     return turn_multiplier * score_material(gs.board)
        return turn_multiplier * score_material(gs.board)

    # move ordering - implement later
    possible_moves_extended = gs.get_all_possible_moves()

    # if depth == DEPTH:
    #     random.shuffle(possible_moves_extended)

    max_score = -255
    m = 0
    for move in possible_moves_extended:
        m += 1
        gs.make_move_extended(move)
        score = -find_move_nega_max_alpha_beta(gs, depth-1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                print(f"m: {m}, counter: {counter}, score: {score}, used time: {(time.time() - current_time)}")

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










move_whole_backup = list()
move_single_backup = list()

# this method has  not been implemented completely yet
def find_move_min_max_alpha_beta_improved_with_cache(gs, depth, alpha, beta):
    global next_move
    global counter



    # if gs.is_game_over():
    #     print(f"GAME OVER works for {'white' if not gs.white_to_move else 'black'}")
    #     return 255 if not gs.white_to_move else -255

    if depth == 0:

        counter += 1
        # return score_material(gs.board)

        possible_moves_extended = gs.get_all_possible_captures()
        if len(possible_moves_extended) > 0:
            depth += 1
        else:
            return score_material(gs.board)
    else:
        possible_moves_extended = gs.get_all_possible_moves()
        if len(possible_moves_extended) == 0:
            counter += 1

            print(f"GAME ENDS AND {'black' if gs.white_to_move else 'white'} wins. Depth: {depth}")
            return -100 if gs.white_to_move else 100

    # possible_moves_extended = gs.get_all_possible_moves()

    # if depth == DEPTH:
    #     random.shuffle(possible_moves_extended)



    move_id = 0

    if depth == DEPTH and len(possible_moves_extended) == 1:
        counter += 1
        next_move = possible_moves_extended[0]
        return


    if gs.white_to_move:
        max_score = -255
        for move in possible_moves_extended:

            # add move ids of related branch
            move_id_as_tuple = tuple(CheckersEngine.get_extended_move_id_list(move))

            move_single_backup.add(tuple(move_id_as_tuple))

            if move_single_backup in move_whole_backup:
                continue
            else:
                move_whole_backup.append(move_single_backup.copy())

            move_id += 1
            gs.make_move_extended(move)
            score = find_move_min_max_alpha_beta_improved(gs, depth - 1, alpha, beta)

            move_single_backup.discard(move_id_as_tuple)

            # print(f"Score: {score}, max_score: {max_score}, depth: {depth}, alpha: {alpha}, beta: {beta}")
            if score > max_score:
                max_score = score
                alpha = max(alpha, max_score)
                if alpha >= beta:
                    gs.undo_move()
                    break

                if depth == DEPTH:
                    next_move = move
                    print(f"turn: {'white'}, move_id: {move_id}, counter: {counter}, score: {score}, used time: {(time.time() - current_time)}")


            gs.undo_move()
        return max_score
    else:
        min_score = 255
        for move in possible_moves_extended:

            # add move ids of related branch
            move_id_as_tuple = tuple(CheckersEngine.get_extended_move_id_list(move))

            move_single_backup.add(tuple(move_id_as_tuple))

            if move_single_backup in move_whole_backup:
                continue
            else:
                move_whole_backup.append(move_single_backup.copy())

            move_id += 1
            gs.make_move_extended(move)
            score = find_move_min_max_alpha_beta_improved(gs, depth - 1, alpha, beta)


            move_single_backup.discard(move_id_as_tuple)



            if score < min_score:
                min_score = score
                beta = min(beta, min_score)
                if beta <= alpha:
                    gs.undo_move()
                    break
                if depth == DEPTH:
                    next_move = move
                    print(f"turn: {'black'}, move_id: {move_id}, counter: {counter}, score: {score}, used time: {(time.time() - current_time)}")
                    if len(possible_moves_extended) == 1:
                        break
            gs.undo_move()
        return min_score