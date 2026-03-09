from __future__ import annotations
from gomoku.board import Board, BLACK, WHITE, EMPTY


class Game:
    """Manages the state of a single Gomoku match.

    Responsibilities:
    - Track whose turn it is.
    - Accept and validate moves.
    - Detect game-over conditions (win or draw).
    - Maintain a move history for undo support.
    """

    def __init__(self) -> None:
        self.board: Board = Board()
        self.current_player: int = BLACK  # BLACK always moves first
        self.winner: int = EMPTY          # EMPTY means no winner yet
        self.move_history: list[tuple[int, int]] = []
        self._game_over: bool = False

    # ------------------------------------------------------------------
    # Core actions
    # ------------------------------------------------------------------

    def make_move(self, row: int, col: int) -> bool:
        """Attempt to place the current player's stone at (row, col).

        Returns True if the move was accepted, False if it was illegal.
        After a successful move the turn advances (or the game ends).
        """
        if self._game_over:
            return False
        if not self.board.is_valid_move(row, col):
            return False

        self.board.place_stone(row, col, self.current_player)
        self.move_history.append((row, col))

        if self.board.check_win(row, col, self.current_player):
            self.winner = self.current_player
            self._game_over = True
        elif self.board.is_full():
            self._game_over = True  # draw — winner stays EMPTY
        else:
            self._switch_player()

        return True

    def undo_move(self) -> bool:
        """Undo the last move and restore the previous turn.

        Returns True if a move was undone, False if there is nothing to undo.
        """
        if not self.move_history:
            return False

        row, col = self.move_history.pop()
        self.board.remove_stone(row, col)

        # Restore state flags
        self._game_over = False
        self.winner = EMPTY
        self._switch_player()  # back to whoever just played

        return True

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def is_over(self) -> bool:
        """Return True when the game has ended (win or draw)."""
        return self._game_over

    def get_winner(self) -> int:
        """Return the winning player (BLACK or WHITE), or EMPTY for a draw
        / ongoing game."""
        return self.winner

    def reset(self) -> None:
        """Reset to a fresh game."""
        self.board.reset()
        self.current_player = BLACK
        self.winner = EMPTY
        self.move_history.clear()
        self._game_over = False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _switch_player(self) -> None:
        self.current_player = WHITE if self.current_player == BLACK else BLACK

    def __repr__(self) -> str:  # pragma: no cover
        player_name = {BLACK: "Black", WHITE: "White", EMPTY: "None"}
        status = (
            f"Winner: {player_name[self.winner]}"
            if self._game_over
            else f"Turn: {player_name[self.current_player]}"
        )
        return f"{self.board!r}\n{status}"
