from __future__ import annotations
from typing import Optional
from gomoku.board import BLACK, WHITE, Board
from gomoku.heuristic import evaluate
from gomoku.move_gen import get_candidate_moves

WIN_SCORE = 1_000_000.0


def _opponent(player: int) -> int:
    return WHITE if player == BLACK else BLACK


def _board_has_five(board: Board, player: int) -> bool:
    for row in range(board.size):
        for col in range(board.size):
            if board.grid[row][col] == player and board.check_win(row, col, player):
                return True
    return False


def _simple_fallback_evaluate(board: Board, player: int) -> float:
    opponent = _opponent(player)
    directions = ((0, 1), (1, 0), (1, 1), (1, -1))

    def score_for(target: int) -> float:
        total = 0.0
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] != target:
                    continue
                for dr, dc in directions:
                    prev_row = row - dr
                    prev_col = col - dc
                    if board.in_bounds(prev_row, prev_col) and board.grid[prev_row][prev_col] == target:
                        continue

                    run = 0
                    next_row, next_col = row, col
                    while board.in_bounds(next_row, next_col) and board.grid[next_row][next_col] == target:
                        run += 1
                        next_row += dr
                        next_col += dc

                    open_ends = 0
                    if board.in_bounds(prev_row, prev_col) and board.grid[prev_row][prev_col] == 0:
                        open_ends += 1
                    if board.in_bounds(next_row, next_col) and board.grid[next_row][next_col] == 0:
                        open_ends += 1

                    if run >= 5:
                        total += WIN_SCORE
                    elif run == 4:
                        total += 15_000 if open_ends == 2 else 4_000
                    elif run == 3:
                        total += 1_500 if open_ends == 2 else 400
                    elif run == 2:
                        total += 150 if open_ends == 2 else 40
                    elif run == 1:
                        total += 10
        return total

    return score_for(player) - score_for(opponent)


def _safe_evaluate(board: Board, player: int) -> float:
    try:
        return float(evaluate(board, player))
    except NotImplementedError:
        return _simple_fallback_evaluate(board, player)


def minimax(
    board: Board,
    depth: int,
    maximizing_player: bool,
    player: int,
) -> tuple[int, Optional[tuple[int, int]]]:

    opponent = _opponent(player)

    if _board_has_five(board, player):
        return int(WIN_SCORE + depth), None
    if _board_has_five(board, opponent):
        return int(-WIN_SCORE - depth), None
    if depth == 0 or board.is_full():
        return int(_safe_evaluate(board, player)), None

    current = player if maximizing_player else opponent
    candidates = get_candidate_moves(board)
    if not candidates:
        return int(_safe_evaluate(board, player)), None

    best_move: Optional[tuple[int, int]] = None
    if maximizing_player:
        best_score = float("-inf")
        for row, col in candidates:
            board.place_stone(row, col, current)
            score, _ = minimax(board, depth - 1, False, player)
            board.remove_stone(row, col)
            if score > best_score:
                best_score = float(score)
                best_move = (row, col)
        return int(best_score), best_move

    best_score = float("inf")
    for row, col in candidates:
        board.place_stone(row, col, current)
        score, _ = minimax(board, depth - 1, True, player)
        board.remove_stone(row, col)
        if score < best_score:
            best_score = float(score)
            best_move = (row, col)
    return int(best_score), best_move


def alphabeta(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    maximizing_player: bool,
    player: int,
) -> tuple[float, Optional[tuple[int, int]]]:
    
    opponent = _opponent(player)

    if _board_has_five(board, player):
        return WIN_SCORE + depth, None
    if _board_has_five(board, opponent):
        return -WIN_SCORE - depth, None
    if depth == 0 or board.is_full():
        return _safe_evaluate(board, player), None

    current = player if maximizing_player else opponent
    candidates = get_candidate_moves(board)
    if not candidates:
        return _safe_evaluate(board, player), None

    best_move: Optional[tuple[int, int]] = None

    if maximizing_player:
        best_score = float("-inf")
        for row, col in candidates:
            board.place_stone(row, col, current)
            score, _ = alphabeta(board, depth - 1, alpha, beta, False, player)
            board.remove_stone(row, col)

            if score > best_score:
                best_score = score
                best_move = (row, col)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        return best_score, best_move

    best_score = float("inf")
    for row, col in candidates:
        board.place_stone(row, col, current)
        score, _ = alphabeta(board, depth - 1, alpha, beta, True, player)
        board.remove_stone(row, col)

        if score < best_score:
            best_score = score
            best_move = (row, col)
        beta = min(beta, best_score)
        if beta <= alpha:
            break

    return best_score, best_move
