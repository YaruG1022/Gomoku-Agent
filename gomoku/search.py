from __future__ import annotations
from typing import Optional
from gomoku.board import BLACK, WHITE, Board
from gomoku.heuristic import evaluate
from gomoku.move_gen import get_candidate_moves

# Score returned when a winning position is found.
WIN_SCORE = 1_000_000.0
# Maximum number of candidate moves evaluated per search node.
MAX_CANDIDATES = 15


def _opponent(player: int) -> int:
    """Return the opponent of *player*."""
    return WHITE if player == BLACK else BLACK


# ---------------------------------------------------------------------------
# Move ordering – improves alpha-beta pruning efficiency
# ---------------------------------------------------------------------------
def _order_moves(
    board: Board,
    candidates: list[tuple[int, int]],
    current: int,
) -> list[tuple[int, int]]:
    """Sort candidates so the most promising moves are examined first.

    Order: immediate wins → blocks of opponent wins → remaining moves.
    Better ordering causes alpha-beta to prune more branches.
    """
    opp = _opponent(current)
    winning: list[tuple[int, int]] = []
    blocking: list[tuple[int, int]] = []
    rest: list[tuple[int, int]] = []

    for row, col in candidates:
        # Check if this move wins immediately for the current player.
        board.place_stone(row, col, current)
        if board.check_win(row, col, current):
            board.remove_stone(row, col)
            winning.append((row, col))
            continue
        board.remove_stone(row, col)

        # Check if this move blocks an immediate win for the opponent.
        board.place_stone(row, col, opp)
        if board.check_win(row, col, opp):
            board.remove_stone(row, col)
            blocking.append((row, col))
            continue
        board.remove_stone(row, col)

        rest.append((row, col))

    # Winning moves first, then blocking moves, then everything else.
    return winning + blocking + rest


# ---------------------------------------------------------------------------
# Minimax (plain, no pruning)
# ---------------------------------------------------------------------------
def minimax(
    board: Board,
    depth: int,
    maximizing_player: bool,
    player: int,
) -> tuple[int, Optional[tuple[int, int]]]:
    """Depth-limited minimax search without alpha-beta pruning.

    Returns (score, best_move).  *player* is the AI whose perspective
    we score from; *maximizing_player* indicates whose turn it is in
    the current node.
    """
    # Leaf node: evaluate the board position with the heuristic.
    if depth == 0 or board.is_full():
        return int(evaluate(board, player)), None

    # Determine who is moving at this node.
    current = player if maximizing_player else _opponent(player)
    candidates = get_candidate_moves(board)
    if not candidates:
        return int(evaluate(board, player)), None

    # Order moves and cap the branching factor.
    candidates = _order_moves(board, candidates, current)[:MAX_CANDIDATES]

    best_move: Optional[tuple[int, int]] = None
    if maximizing_player:
        # AI's turn: pick the move with the highest score.
        best_score = float("-inf")
        for row, col in candidates:
            board.place_stone(row, col, current)
            # Early termination: if this move wins, return immediately.
            if board.check_win(row, col, current):
                board.remove_stone(row, col)
                return int(WIN_SCORE + depth), (row, col)
            # Recurse with the opponent as the minimizing player.
            score, _ = minimax(board, depth - 1, False, player)
            board.remove_stone(row, col)
            if score > best_score:
                best_score = float(score)
                best_move = (row, col)
        return int(best_score), best_move

    # Opponent's turn: pick the move with the lowest score (worst for AI).
    best_score = float("inf")
    for row, col in candidates:
        board.place_stone(row, col, current)
        # Early termination: opponent wins.
        if board.check_win(row, col, current):
            board.remove_stone(row, col)
            return int(-WIN_SCORE - depth), (row, col)
        # Recurse with the AI as the maximizing player.
        score, _ = minimax(board, depth - 1, True, player)
        board.remove_stone(row, col)
        if score < best_score:
            best_score = float(score)
            best_move = (row, col)
    return int(best_score), best_move


# ---------------------------------------------------------------------------
# Alpha-Beta pruning (optimised minimax)
# ---------------------------------------------------------------------------
def alphabeta(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    maximizing_player: bool,
    player: int,
) -> tuple[float, Optional[tuple[int, int]]]:
    """Minimax search with alpha-beta pruning.

    *alpha* - the best score the maximizer can guarantee so far.
    *beta*  - the best score the minimizer can guarantee so far.
    When beta <= alpha the remaining branches cannot affect the result
    and are pruned (skipped).

    Returns (score, best_move).
    """
    # Leaf node: fall back to the heuristic evaluation.
    if depth == 0 or board.is_full():
        return evaluate(board, player), None

    # Determine who is moving at this node.
    current = player if maximizing_player else _opponent(player)
    candidates = get_candidate_moves(board)
    if not candidates:
        return evaluate(board, player), None

    # Order moves for better pruning, then cap the branching factor.
    candidates = _order_moves(board, candidates, current)[:MAX_CANDIDATES]

    best_move: Optional[tuple[int, int]] = None

    if maximizing_player:
        # AI's turn: try to maximise the score.
        best_score = float("-inf")
        for row, col in candidates:
            board.place_stone(row, col, current)
            # Immediate win – no need to search deeper.
            if board.check_win(row, col, current):
                board.remove_stone(row, col)
                # +depth so shallower (faster) wins score higher.
                return WIN_SCORE + depth, (row, col)
            # Recurse: opponent tries to minimise.
            score, _ = alphabeta(board, depth - 1, alpha, beta, False, player)
            board.remove_stone(row, col)

            if score > best_score:
                best_score = score
                best_move = (row, col)
            # Raise the lower bound (maximizer's guarantee).
            alpha = max(alpha, best_score)
            # Prune: the minimizer above would never allow this path.
            if beta <= alpha:
                break

        return best_score, best_move

    # Opponent's turn: try to minimise the score.
    best_score = float("inf")
    for row, col in candidates:
        board.place_stone(row, col, current)
        # Immediate opponent win.
        if board.check_win(row, col, current):
            board.remove_stone(row, col)
            return -WIN_SCORE - depth, (row, col)
        # Recurse: AI tries to maximise.
        score, _ = alphabeta(board, depth - 1, alpha, beta, True, player)
        board.remove_stone(row, col)

        if score < best_score:
            best_score = score
            best_move = (row, col)
        # Lower the upper bound (minimizer's guarantee).
        beta = min(beta, best_score)
        # Prune: the maximizer above would never choose this path.
        if beta <= alpha:
            break

    return best_score, best_move
