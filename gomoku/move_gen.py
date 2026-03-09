from __future__ import annotations
from gomoku.board import Board, EMPTY


def get_candidate_moves(
    board: Board,
    radius: int = 2,
) -> list[tuple[int, int]]:
    """Return a list of candidate (row, col) moves worth considering.

    Instead of returning every empty cell, only cells within *radius*
    squares of an already-placed stone are returned.  This dramatically
    reduces the branching factor without missing strong moves.

    Falls back to the centre cell when the board is completely empty.

    Parameters
    ----------
    board:
        Current board state.
    radius:
        Manhattan neighbourhood radius around existing stones to include.
    """
    # TODO: iterate over all non-empty cells
    # TODO: for each stone, add empty neighbours within *radius* to a set
    # TODO: return sorted / deduplicated candidate list
    raise NotImplementedError
