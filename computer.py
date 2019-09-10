import random
from board import ROW_COUNT, COLUMN_COUNT

CENTER_COLUMN_MOVE = 2
TWO_WIN_MOVE = 3
ONE_WIN_MOVE = 7
WINNING_MOVE = 10000


class ComputerPlayer:

    def __init__(self, difficulty, board):
        self.depth = difficulty - 1
        self.board = board

    # If there is no best move then random column is generated
    def get_random_column(self):
        ran_col = random.randint(0, COLUMN_COUNT - 1)
        return ran_col

    # Evaluates possible moves and scores each outcome returning the best move
    def evaluate_move(self, player_tile, opponent_tile):
        valid_locations = self.get_valid_locations()
        highest_score = 0
        for move in valid_locations:
            if isinstance(move[0], int) and isinstance(move[1], int):
                row = move[0]
                col = move[1]
                score = 0
                # Creates groups of 4 groups of 3 around each possible move and calculates score for each
                for x in range(3):
                    adj_col = col + x
                    adj_row = row + x
                    if adj_col < COLUMN_COUNT and adj_col - 3 >= 0:
                        hor_group = [self.board[row, adj_col], self.board[row, adj_col - 1],
                                     self.board[row, adj_col - 2], self.board[row, adj_col - 3]]
                        score += self.calculate_score(hor_group, player_tile, opponent_tile)

                    if adj_row < ROW_COUNT and adj_row - 3 >= 0:
                        vert_group = [self.board[adj_row, col], self.board[adj_row - 1, col],
                                      self.board[adj_row - 2, col], self.board[adj_row - 3, col]]
                        score += self.calculate_score(vert_group, player_tile, opponent_tile)

                    if adj_col < COLUMN_COUNT and adj_col - 3 >= 0 and adj_row < ROW_COUNT and adj_row - 3 >= 0:
                        diag_group = [self.board[adj_row, adj_col], self.board[adj_row - 1, adj_col - 1],
                                      self.board[adj_row - 2, adj_col - 2], self.board[adj_row - 3, adj_col - 3]]
                        score += self.calculate_score(diag_group, player_tile, opponent_tile)

                # If center column is open then score it accordingly
                if col == 3 and self.is_valid_location(col):
                    score += CENTER_COLUMN_MOVE

                # If score is highest then set score and best move
                if score > highest_score:
                    highest_score = score
                    best_move = col

        # If no move had any score then make a random move
        if highest_score == 0:
            col = self.get_random_column()
            while not self.is_valid_location(col):
                col = self.get_random_column()
            best_move = col

        return best_move

    # Calculate the score in each group based on how many tiles move is away from win
    def calculate_score(self, group, player_tile, opponent_tile):
        score = 0
        num_player_tiles = 0
        if opponent_tile not in group:
            for tile in group:
                if tile == player_tile:
                    num_player_tiles += 1
            if num_player_tiles == 2:
                score += TWO_WIN_MOVE
            elif num_player_tiles == 3:
                score += ONE_WIN_MOVE
            elif num_player_tiles == 4:
                score += WINNING_MOVE
        return score

    def get_valid_locations(self):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if self.is_valid_location(col):
                row = self.get_next_open_row(col)
                valid_locations.append([row, col])
            else:
                valid_locations.append(['x', 'x'])
        return valid_locations

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def is_valid_location(self, col):
        return self.board[ROW_COUNT - 1][col] == 0
