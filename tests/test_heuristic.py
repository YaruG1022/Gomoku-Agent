from __future__ import annotations

from gomoku.board import BLACK, WHITE, Board
from gomoku.heuristic import WIN_SCORE, evaluate


def test_evaluate_detects_five_in_a_row() -> None:
	board = Board()
	for col in range(5):
		board.place_stone(7, col, BLACK)

	assert evaluate(board, BLACK) >= WIN_SCORE
	assert evaluate(board, WHITE) <= -WIN_SCORE


def test_open_four_scores_higher_than_open_three() -> None:
	open_three = Board()
	for col in range(5, 8):
		open_three.place_stone(7, col, BLACK)

	open_four = Board()
	for col in range(5, 9):
		open_four.place_stone(7, col, BLACK)

	assert evaluate(open_four, BLACK) > evaluate(open_three, BLACK)


def test_opponent_threat_reduces_score() -> None:
	board = Board()
	for col in range(4, 8):
		board.place_stone(7, col, WHITE)

	assert evaluate(board, BLACK) < 0
	assert evaluate(board, WHITE) > 0
