from __future__ import annotations
from gomoku.board import BLACK, EMPTY, WHITE, Board

WIN_SCORE = 1_000_000
PATTERN_SCORES: dict[tuple[int, int], int] = {
    (4, 2): 100_000, # open four: 0XXXX0
    (4, 1): 10_000,  # half-open four: 0XXXXO or OXXXX0
    (3, 2): 2_000,   # open three: 0XXX0
    (3, 1): 300,     # half-open three: 0XXXO or OXXX0
    (2, 2): 120,     # open two: 0XX0
    (2, 1): 20,      # half-open two: 0XXO or OXX0
    (1, 2): 8,       # open one: 0X0
    (1, 1): 2,       # half-open one: 0XO or OX0
}


def _opponent(player: int) -> int:
    """Return the opponent of *player*."""
    return WHITE if player == BLACK else BLACK


def _score_lines(board: Board, target: int) -> float:
    """Calculate the score for *target* based on patterns of stones on the board."""
    score = 0.0
    directions = ((0, 1), (1, 0), (1, 1), (1, -1))

    for row in range(board.size):
        for col in range(board.size):
            if board.grid[row][col] != target:
                continue

            for dr, dc in directions:
                prev_row = row - dr
                prev_col = col - dc
                if board.in_bounds(prev_row, prev_col) and board.grid[prev_row][prev_col] == target:
                    continue

                run_length = 0
                next_row, next_col = row, col
                while board.in_bounds(next_row, next_col) and board.grid[next_row][next_col] == target:
                    run_length += 1
                    next_row += dr
                    next_col += dc

                open_ends = 0
                if board.in_bounds(prev_row, prev_col) and board.grid[prev_row][prev_col] == EMPTY:
                    open_ends += 1
                if board.in_bounds(next_row, next_col) and board.grid[next_row][next_col] == EMPTY:
                    open_ends += 1

                if run_length >= 5:
                    score += WIN_SCORE
                    continue

                score += PATTERN_SCORES.get((run_length, open_ends), 0)

    return score


def evaluate(board: Board, player: int) -> float:
    """Return a heuristic score for *board* from *player*'s perspective.

    A higher score is better for *player*; a lower (more negative) score
    is better for the opponent.

    This is a placeholder — implement pattern-based scoring here.
    Common patterns to score:
    - Open / half-open fours
    - Open / half-open threes
    - Blocked twos
    - Immediate winning threats (five-in-a-row)
    """

    player_score = _score_lines(board, player)
    opponent_score = _score_lines(board, _opponent(player))
    return player_score - opponent_score * 1.05
