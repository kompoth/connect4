import numpy as np

# Max values are limited only by the output,
# might be easily extended

MIN_DIM = 1
MAX_DIM = 9
MIN_PLAYERS = 0
MAX_PLAYERS = 9


class Game:
    def __init__(self, players: int = 2, cols: int = 7, rows: int = 6) -> None:
        if not MIN_PLAYERS <= players <= MAX_PLAYERS:
            raise ValueError(f"Unsupported number of players: {players}")
        if not MIN_DIM <= cols <= MAX_DIM or not MIN_DIM <= rows <= MAX_DIM:
            raise ValueError(f"Unsupported dimensions: {cols}x{rows}")
        self.queue = list(range(1, players + 1))
        self.board = np.zeros((rows, cols), dtype=int)
        self.rows = rows
        self.cols = cols

    def __repr__(self) -> str:
        res = f"Queue: {self.queue}\n  |"
        res += "|".join(str(x) for x in range(1, self.cols + 1))
        res += "|\n"
        for row_no in range(1, self.rows + 1):
            res += f"{row_no:2}|"
            cell_strings = [
                " " if x == 0 else str(x)
                for x in self.board[row_no - 1]
            ]
            res += "|".join(cell_strings)
            res += "|\n"
        return res

    def move(self, col: int, row: int) -> int | None:
        if not MIN_DIM <= col <= self.cols or not MIN_DIM <= row <= self.rows:
            raise ValueError(f"Wrong cell coordinates: {col} {row}")
        if self.board[col, row] != 0:
            raise ValueError(f"Occupied cell: {col} {row}")
        col -= 1
        row -= 1

        # Fall
        rows_to_check = range(row + 1, self.rows)
        fall_row = row
        for next_row in rows_to_check:
            if self.board[next_row, col] != 0:
                break
            else:
                fall_row = next_row

        # Update board
        player = self.queue.pop(0)
        self.queue.append(player)
        self.board[fall_row, col] = player

        # Chech for the winner
        winner_rows = self.check_rows()
        winner_cols = self.check_cols()
        winner_dias = self.check_dias()
        if winner_rows is not None:
            return winner_rows
        if winner_cols is not None:
            return winner_cols
        if winner_dias is not None:
            return winner_dias
        return None

    def check_rows(self) -> int | None:
        for row in range(self.rows):
            count = 1
            cur_val = 0
            for col in range(self.cols):
                cell = self.board[row, col]
                if cur_val == cell:
                    count += 1
                    if count >= 4 and cell != 0:
                        return cell
                else:
                    count = 0
                    cur_val = cell
        return None

    def check_cols(self) -> int | None:
        for col in range(self.cols):
            count = 1
            prev_val = 0
            for row in range(self.rows):
                cell = self.board[row, col]
                if prev_val == cell:
                    count += 1
                    if count >= 4 and cell != 0:
                        return cell
                else:
                    count = 1
                    prev_val = cell
        return None

    def check_dias(self) -> int | None:
        # Не успел, принцип тот же
        pass


if __name__ == "__main__":
    g = Game()
    done = False
    while True:
        print(g)
        player = g.queue[0]
        row, col = input(f"Player {player}, enter column and row: ").split()
        winner = g.move(int(row), int(col))
        if winner is not None:
            print(f"Player {winner} won")
            break
