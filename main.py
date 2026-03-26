from __future__ import annotations

import sys
from typing import Optional

import pygame

from gomoku.board import BLACK, EMPTY, WHITE
from gomoku.game import Game
from gomoku.move_gen import get_candidate_moves

WINDOW_SIZE = 760
GRID_MARGIN = 60
STATUS_HEIGHT = 72
STONE_RADIUS = 18
BOARD_COLOR = (214, 184, 132)
LINE_COLOR = (66, 46, 28)
BACKGROUND_COLOR = (241, 232, 210)
BLACK_STONE_COLOR = (30, 30, 30)
WHITE_STONE_COLOR = (243, 243, 243)
HIGHLIGHT_COLOR = (188, 61, 44)
TEXT_COLOR = (32, 32, 32)


def choose_ai_move(game: Game, ai_player: int) -> Optional[tuple[int, int]]:
    candidates = get_candidate_moves(game.board)
    if not candidates:
        return None

    opponent = BLACK if ai_player == WHITE else WHITE

    for row, col in candidates:
        game.board.place_stone(row, col, ai_player)
        is_winning_move = game.board.check_win(row, col, ai_player)
        game.board.remove_stone(row, col)
        if is_winning_move:
            return (row, col)

    for row, col in candidates:
        game.board.place_stone(row, col, opponent)
        must_block = game.board.check_win(row, col, opponent)
        game.board.remove_stone(row, col)
        if must_block:
            return (row, col)

    center = game.board.size // 2
    return min(
        candidates,
        key=lambda move: (abs(move[0] - center) + abs(move[1] - center), move[0], move[1]),
    )


def draw_board(screen: pygame.Surface, game: Game, font: pygame.font.Font) -> None:
    screen.fill(BACKGROUND_COLOR)
    board_rect = pygame.Rect(0, 0, WINDOW_SIZE, WINDOW_SIZE)
    pygame.draw.rect(screen, BOARD_COLOR, board_rect)

    cell_size = (WINDOW_SIZE - 2 * GRID_MARGIN) / (game.board.size - 1)

    for index in range(game.board.size):
        offset = GRID_MARGIN + index * cell_size
        pygame.draw.line(screen, LINE_COLOR, (GRID_MARGIN, offset), (WINDOW_SIZE - GRID_MARGIN, offset), 2)
        pygame.draw.line(screen, LINE_COLOR, (offset, GRID_MARGIN), (offset, WINDOW_SIZE - GRID_MARGIN), 2)

    for row in range(game.board.size):
        for col in range(game.board.size):
            value = game.board.grid[row][col]
            if value == EMPTY:
                continue

            center_x = int(GRID_MARGIN + col * cell_size)
            center_y = int(GRID_MARGIN + row * cell_size)
            stone_color = BLACK_STONE_COLOR if value == BLACK else WHITE_STONE_COLOR
            pygame.draw.circle(screen, stone_color, (center_x, center_y), STONE_RADIUS)
            pygame.draw.circle(screen, LINE_COLOR, (center_x, center_y), STONE_RADIUS, 1)

    if game.move_history:
        last_row, last_col = game.move_history[-1]
        center_x = int(GRID_MARGIN + last_col * cell_size)
        center_y = int(GRID_MARGIN + last_row * cell_size)
        pygame.draw.circle(screen, HIGHLIGHT_COLOR, (center_x, center_y), 5)

    status_top = WINDOW_SIZE
    pygame.draw.rect(screen, BACKGROUND_COLOR, (0, status_top, WINDOW_SIZE, STATUS_HEIGHT))

    if game.is_over():
        if game.get_winner() == EMPTY:
            status_text = "Draw. Press R to restart."
        elif game.get_winner() == BLACK:
            status_text = "Black wins. Press R to restart."
        else:
            status_text = "White wins. Press R to restart."
    else:
        player_name = "Black" if game.current_player == BLACK else "White"
        status_text = f"Turn: {player_name}. R: restart, U: undo"

    text_surface = font.render(status_text, True, TEXT_COLOR)
    screen.blit(text_surface, (24, status_top + 22))


def screen_to_move(position: tuple[int, int], board_size: int) -> Optional[tuple[int, int]]:
    x_pos, y_pos = position
    if x_pos < GRID_MARGIN - 18 or x_pos > WINDOW_SIZE - GRID_MARGIN + 18:
        return None
    if y_pos < GRID_MARGIN - 18 or y_pos > WINDOW_SIZE - GRID_MARGIN + 18:
        return None

    cell_size = (WINDOW_SIZE - 2 * GRID_MARGIN) / (board_size - 1)
    col = round((x_pos - GRID_MARGIN) / cell_size)
    row = round((y_pos - GRID_MARGIN) / cell_size)
    if 0 <= row < board_size and 0 <= col < board_size:
        return (row, col)
    return None


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Gomoku Agent")
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + STATUS_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("segoeui", 24)

    game = Game()
    human_player = BLACK
    ai_player = WHITE

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                elif event.key == pygame.K_u:
                    if game.move_history:
                        game.undo_move()
                    if game.move_history and game.current_player == ai_player:
                        game.undo_move()

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and not game.is_over()
                and game.current_player == human_player
            ):
                move = screen_to_move(event.pos, game.board.size)
                if move is not None:
                    game.make_move(*move)

        if not game.is_over() and game.current_player == ai_player:
            ai_move = choose_ai_move(game, ai_player)
            if ai_move is not None:
                game.make_move(*ai_move)

        draw_board(screen, game, font)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
