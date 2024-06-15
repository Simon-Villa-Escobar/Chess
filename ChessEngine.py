"""
This class is responsible for storing all the
information about the current state of a chess game.
It will also be responsible for determining the valid moves at the current state.
"""


class GameState:
    def __init__(self):
        # A chess board is a 8x8 2d list, each element of the list has two characters.
        # The first character represents the color of the piece, 'b' or 'w'
        # The second character represents the type of the piece 'K,', 'Q', 'R', 'B', 'N', or 'p'
        # '--' represents an empty space with no piece

        self.board = [
            [
                "bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"
            ],
            [
                "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"
            ],
            [
                "--", "--", "--", "--", "--", "--", "--", "--"
            ],
            [
                "--", "--", "--", "--", "--", "--", "--", "--"
            ],
            [
                "--", "--", "--", "--", "--", "--", "--", "--"
            ],
            [
                "--", "--", "--", "--", "--", "--", "bp", "--"
            ],
            [
                "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"
            ],
            [
                "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"
            ],
        ]
        self.move_functions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}

        self.whiteToMove = True
        self.moveLog = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)  # Log the move
        self.whiteToMove = not self.whiteToMove

    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.whiteToMove = not self.whiteToMove

    def get_valid_moves(self):
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if (c-1) >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if (c+1) <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))

    def get_rook_moves(self, r, c, moves):
        pass

    def get_knight_moves(self, r, c, moves):
        pass

    def get_bishop_moves(self, r, c, moves):
        pass

    def get_queen_moves(self, r, c, moves):
        pass

    def get_king_moves(self, r, c, moves):
        pass

class Move:
    #   maps keys to values
    #   key : value

    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        # print(self.move_id)

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False


    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
