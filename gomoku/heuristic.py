from __future__ import annotations
from gomoku.board import Board


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

    raise NotImplementedError
