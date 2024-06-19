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
                "--", "--", "--", "--", "--", "--", "--", "--"
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
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.check_mate = False
        self.stale_mate = False
        self.in_check = False
        self.pins = []
        self.checks = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)  # Log the move
        self.whiteToMove = not self.whiteToMove
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.whiteToMove = not self.whiteToMove
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)

    # def get_valid_moves(self):
    #     #1  Generate all possibles moves
    #     moves = self.get_all_possible_moves()
    #     #2  For each move, make the move
    #     for i in range(len(moves)-1, -1, -1):
    #         self.make_move(moves[i])
    #         #3  Generate all opponent's moves
    #         #4  For each of your opponent's moves, see if they attack your king
    #         self.whiteToMove = not self.whiteToMove
    #         if self.in_check():
    #             moves.remove(moves[i])
    #         self.whiteToMove = not self.whiteToMove
    #         self.undo_move()
    #     if len(moves) == 0:
    #         if self.in_check():
    #             self.check_mate = True
    #         else:
    #             self.stale_mate = True
    #     else:
    #         self.check_mate = False
    #         self.stale_mate = False
    #     return moves

    def get_valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.whiteToMove:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1:
                moves = self.get_all_possible_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []
                if piece_checking[1] == 'N':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != 'K':
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_all_possible_moves()

        return moves

    def check_for_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        if self.whiteToMove:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        type = end_piece[1]

                        if (0 <= j <= 3 and type == 'R') or (4 <= j <= 7 and type == 'B') or (
                                i == 1 and type == 'p' and (
                                (enemy_color == 'w' and 6 <= j <= 7) or (enemy_color == 'b' and 4 <= j <= 5))) or (
                                type == 'Q') or (i == 1 and type == 'K'):
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else:
                    break

        knight_moves = ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))
        return in_check, pins, checks

    def in_check(self):
        if self.whiteToMove:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        opp_moves = self.get_all_possible_moves()
        self.whiteToMove = not self.whiteToMove
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False

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
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            if r > 0 and self.board[r - 1][c] == "--":
                if not piece_pinned or pin_direction == (-1, 0):
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == "--":
                        moves.append(Move((r, c), (r - 2, c), self.board))
            if r > 0 and (c - 1) >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    if not piece_pinned or pin_direction == (-1, -1):
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if r > 0 and (c + 1) <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    if not piece_pinned or pin_direction == (-1, 1):
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if r < 7 and self.board[r + 1][c] == "--":
                if not piece_pinned or pin_direction == (1, 0):
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move((r, c), (r + 2, c), self.board))
            if r < 7 and (c - 1) >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    if not piece_pinned or pin_direction == (1, -1):
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if r < 7 and (c + 1) <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    if not piece_pinned or pin_direction == (1, 1):
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))

    # def multiple_moves(self, directions, r, c, moves):
    #     piece_pinned = False
    #     pin_direction = ()
    #     for i in range(len(self.pins) - 1, -1, -1):
    #         if self.pins[i][0] == r and self.pins[i][1] == c:
    #             piece_pinned = True
    #             pin_direction = (self.pins[i][2], self.pins[i][3])
    #             if self.board[r][c][1] != 'Q':
    #                 self.pins.remove(self.pins[i])
    #             break
    #
    #     enemy_color = 'b' if self.whiteToMove else 'w'
    #     for d in directions:
    #         for i in range(1, 8):
    #             end_row, end_col = r + d[0] * i, c + d[1] * i
    #             if 0 <= end_row < 8 and 0 <= end_col < 8:  # Check boundaries
    #                 if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
    #                     end_piece = self.board[end_row][end_col]
    #                     if end_piece == "--":  # Empty space
    #                         moves.append(Move((r, c), (end_row, end_col), self.board))
    #                     elif end_piece[0] == enemy_color:  # Enemy piece
    #                         moves.append(Move((r, c), (end_row, end_col), self.board))
    #                         break
    #                     else:  # Friendly piece
    #                         break
    #             else:
    #                 break

    # def single_move(self, directions, r, c, moves):
    #     piece_pinned = False
    #     pin_direction = ()
    #     for i in range(len(self.pins) - 1, -1, -1):
    #         if self.pins[i][0] == r and self.pins[i][1] == c:
    #             piece_pinned = True
    #             self.pins.remove(self.pins[i])
    #             break
    #
    #     ally_color = 'w' if self.whiteToMove else 'b'
    #     for d in directions:
    #         end_row, end_col = r + d[0], c + d[1]
    #         if 0 <= end_row < 8 and 0 <= end_col < 8:
    #             if not piece_pinned:
    #                 end_piece = self.board[end_row][end_col]
    #                 if end_piece[0] != ally_color:
    #                     moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_rook_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # down, up, right, left
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row, end_col = r + d[0] * i, c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # Check boundaries
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # Empty space
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # Enemy piece
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else:  # Friendly piece
                            break
                else:
                    break

    def get_knight_moves(self, r, c, moves):
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        ally_color = 'w' if self.whiteToMove else 'b'
        for d in directions:
            end_row, end_col = r + d[0], c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row, end_col = r + d[0] * i, c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # Check boundaries
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # Empty space
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # Enemy piece
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else:  # Friendly piece
                            break
                else:
                    break

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    def get_king_moves(self, r, c, moves):
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.whiteToMove else "b"
        for i in range(8):
            end_row = r + row_moves[i]
            end_col = c + col_moves[i]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    if ally_color == "w":
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    if ally_color == "w":
                        self.white_king_location = (r, c)
                    else:
                        self.black_king_location = (r, c)


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
