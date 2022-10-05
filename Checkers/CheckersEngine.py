"""
This class is responsible for storing all the information about the current state of a chess game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""


class GameState:
    def __init__(self):
        # board is a 10x10 2d list, each element of the list has 2 characters.
        # the first character represents the color of the piece, 'b' or 'w'
        # the second character represents the type of the piece, p, k
        # "--" - represents an empty space with no piece
        # Note: list will be converted to numpy array for efficiency later
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

        self.white_to_move = True
        self.move_log = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # log the move so we can undo it later
        self.white_to_move = not self.white_to_move  # switch turns

    # Undo the last move made
    def undo_move(self):
        if len(self.move_log):  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move  # switch turns

    # All moves considering rules (for e., the move that captures the greatest number of pieces must be made.)
    def get_valid_moves(self):
        return self.get_all_possible_moves()  # for now, we will not worry about some rules

    # All moves without considering rules
    def get_all_possible_moves(self):
        moves = [Move((6, 5), (4, 5), self.board)]
        for row in range(len(self.board)):  # number of rows
            for col in range(len(self.board[row])):  # number of cols in given row
                turn = self.board[row][col][0]
                if turn == "w" and self.white_to_move or turn == "b" and not self.white_to_move:
                    piece = self.board[row][col][1]
                    if piece == "m":
                        pass
                    elif piece == "k":
                        pass
        return moves

    # Get all the man moves for the man located at row, col and add these moves to the list
    def get_man_moves(self, row, col, moves):
        pass

    # Get all the king moves for the king located at row, col and add these moves to the list
    def get_king_moves(self, row, col, moves):
        pass


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

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        print(self.move_id)

    def get_checkers_notation(self):
        return self.get_square_position(self.start_row, self.start_col), \
               self.get_square_position(self.end_row, self.end_col)

    def get_square_position(self, row, col):
        # if (row, col) in self.row_col_to_square_position:
        return self.row_col_to_square_position[(row, col)]

    # Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False
