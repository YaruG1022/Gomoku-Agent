from __future__ import annotations
from typing import Optional
from gomoku.board import Board


def minimax(
    board: Board,
    depth: int,
    maximizing_player: bool,
    player: int,
) -> tuple[int, Optional[tuple[int, int]]]:
    """Minimax search skeleton.

    Parameters
    ----------
    board:
        Current board state.
    depth:
        Remaining search depth. Returns a heuristic evaluation when 0.
    maximizing_player:
        True if it is the maximising player's turn.
    player:
        The perspective player used for heuristic evaluation.

    Returns
    -------
    (score, best_move)
        *score* is the evaluated value of the position.
        *best_move* is (row, col) of the best move found, or None at leaf nodes.
    """
    # TODO: implement terminal check (win / draw)
    # TODO: evaluate leaf nodes with heuristic.evaluate()
    # TODO: generate candidate moves with move_gen.get_candidate_moves()
    # TODO: recurse for each candidate, updating best_score / best_move
    raise NotImplementedError


def alphabeta(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    maximizing_player: bool,
    player: int,
) -> tuple[float, Optional[tuple[int, int]]]:
    """Minimax with alpha-beta pruning skeleton.

    Parameters
    ----------
    board:
        Current board state.
    depth:
        Remaining search depth.
    alpha:
        Best value the maximiser can currently guarantee.
    beta:
        Best value the minimiser can currently guarantee.
    maximizing_player:
        True if it is the maximising player's turn.
    player:
        The perspective player used for heuristic evaluation.

    Returns
    -------
    (score, best_move)
        *score* is the evaluated value of the position.
        *best_move* is (row, col) of the best move found, or None at leaf nodes.
    """
    # TODO: implement terminal check (win / draw)
    # TODO: evaluate leaf nodes with heuristic.evaluate()
    # TODO: generate candidate moves with move_gen.get_candidate_moves()
    # TODO: recurse for each candidate
    # TODO: prune when beta <= alpha
    raise NotImplementedError
