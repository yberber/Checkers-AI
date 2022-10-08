"""
This class is responsible for storing all the information about the current state of a chess game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""


# Get a given data from a dictionary with position provided as a list
def nested_get(dic, keys):
    for key in keys:
        dic = dic[key]
    return dic


# Set a given data in a dictionary with position provided as a list
def nested_set(dic, keys, value):
    for key in keys[:-1]:
        # dic = dic.setdefault(key, {})  # an alternative which throws no error
        dic = dic[key]  # this one throws error if key dies not exists in the  dictionary
    dic[keys[-1]] = value


class GameState:
    def __init__(self):
        # board is a 10x10 2d list, each element of the list has 2 characters.
        # the first character represents the color of the piece, 'b' or 'w'
        # the second character represents the type of the piece, p, k
        # "--" - represents an empty space with no piece
        # Note: list will be converted to numpy array for efficiency later
        self.valid_moves = None
        self.board = [
            ["--", "bm", "--", "bm", "--", "bm", "--", "bm", "--", "bm"],
            ["bm", "--", "bm", "--", "bm", "--", "bm", "--", "bm", "--"],
            ["--", "bm", "--", "bm", "--", "bm", "--", "bm", "--", "bm"],
            ["bm", "--", "bm", "--", "bm", "--", "bm", "--", "bm", "--"],

            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],

            ["--", "wm", "--", "wm", "--", "wm", "--", "wm", "--", "wm"],
            ["wm", "--", "wm", "--", "wm", "--", "wm", "--", "wm", "--"],
            ["--", "wm", "--", "wm", "--", "wm", "--", "wm", "--", "wm"],
            ["wm", "--", "wm", "--", "wm", "--", "wm", "--", "wm", "--"]
        ]

        self.move_functions = {'m': self.get_man_moves, 'k': self.get_king_moves}
        self.capture_functions = {'m': self.get_man_captures, 'k': self.get_king_captures}

        self.white_to_move = True
        self.move_log = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        if move.captured_piece != "--":
            row, col = move.captured_piece_pos
            self.board[row][col] = "--"
        self.move_log.append(move)  # log the move so we can undo it later
        self.white_to_move = not self.white_to_move  # switch turns

    # Undo the last move made
    def undo_move(self):
        if len(self.move_log):  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.captured_piece
            self.white_to_move = not self.white_to_move  # switch turns

    def undo_move_by_move(self, move):
        self.board[move.start_row][move.start_col] = move.piece_moved
        self.board[move.end_row][move.end_col] = move.captured_piece
        if move.captured_piece != "--":
            self.board[move.captured_piece_pos[0]][move.captured_piece_pos[1]] = move.captured_piece
        self.white_to_move = not self.white_to_move  # switch turns

    # All moves considering rules (for e., the move that captures the greatest number of pieces must be made.)
    def get_valid_moves(self):
        self.valid_moves = self.get_all_possible_moves()
        return self.valid_moves  # for now, we will not worry about some rules

    def get_valid_moves_for_selected_piece(self, sq_selected):
        valid_moves_for_selected_piece = []
        for move in self.valid_moves:
            if sq_selected == (move.start_row, move.start_col):
                valid_moves_for_selected_piece.append(move)
        return valid_moves_for_selected_piece

    # All moves without considering rules
    def get_all_possible_moves(self):
        moves = []
        moves_with_captures = []
        for row in range(len(self.board)):  # number of rows
            for col in range(len(self.board[row])):  # number of cols in given row
                turn = self.board[row][col][0]
                if turn == "w" and self.white_to_move or turn == "b" and not self.white_to_move:
                    piece = self.board[row][col][1]
                    self.capture_functions[piece](row, col, moves_with_captures)
                    self.move_functions[piece](row, col, moves)

        if len(moves_with_captures) != 0:
            return moves_with_captures

        return moves

    # Get all the man moves for the man located at row, col and add these moves to the list
    def get_man_moves(self, row, col, moves):
        forward_direction = -1 if self.white_to_move else 1
        directions = ((forward_direction, -1), (forward_direction, 1))

        for d in directions:
            end_row = row + d[0]
            end_col = col + d[1]
            if self.is_on_board(end_row, end_col) and self.board[end_row][end_col] == "--":
                moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_man_captures(self, row, col, moves_with_captures, enemy_color=None):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if enemy_color is None:
            enemy_color = "b" if self.white_to_move else "w"
        # ally_color = "w" if self.white_to_move else "b"
        for d in directions:
            end_row = row + 2 * d[0]
            end_col = col + 2 * d[1]
            if self.is_on_board(end_row, end_col) and self.board[end_row][end_col] == "--":
                next_row = row + d[0]
                next_col = col + d[1]
                piece = self.board[next_row][next_col]
                if piece[0] == enemy_color:
                    moves_with_captures.append(Move((row, col), (end_row, end_col), self.board, piece,
                                                    (next_row, next_col)))


    def find_captures_by_directions(self, row, col, enemy_color, directions):
        pass

    # Get all the king moves for the king located at row, col and add these moves to the list
    def get_king_moves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        for d in directions:
            for i in range(1, 10):
                end_row = row + d * i
                end_col = col + d * i
                if self.is_on_board(end_row, end_col):  # on board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # empty space valid
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    else:
                        break
                else:
                    break

    def get_king_captures(self, row, col, moves_with_captures):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = "b" if self.white_to_move else "w"
        pass

    @staticmethod
    def is_on_board(row, col):
        return 0 <= row < 10 and 0 <= col < 10


# Takes a move as a parameter and executes it.
class Move:
    dimension = 10  # make this variable static constant in a python file which stores constant variables
    square_position_to_row_col = {}
    row_col_to_square_position = {}
    pos = 1
    for row in range(dimension):
        for col in range(dimension):
            if (row + col) % 2:
                square_position_to_row_col[pos] = (row, col)
                row_col_to_square_position[(row, col)] = pos
                pos += 1

    def __init__(self, start_sq, end_sq, board, captured_piece="--", captured_piece_pos=None):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.captured_piece = captured_piece
        self.captured_piece_pos = captured_piece_pos
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def get_checkers_notation(self):
        return self.get_square_position(self.start_row, self.start_col), \
               self.get_square_position(self.end_row, self.end_col)

    def get_square_position(self, row, col):
        if (row, col) in self.row_col_to_square_position:
            return self.row_col_to_square_position[(row, col)]

    # Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id

    def __str__(self):
        return f"({self.start_row}, {self.start_col}) -> ({self.end_row}, {self.end_col}),  " \
               f"x({self.captured_piece})"

