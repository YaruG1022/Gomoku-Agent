# Gomoku-Agent

A Python-based Gomoku (Five-in-a-Row) game-playing agent featuring a depth-limited
Minimax search with Alpha-Beta pruning and a pattern-based heuristic evaluation
function, playable on a 15×15 board.

## Project Structure

```
Gomoku-Agent/
├── gomoku/              # Core package
│   ├── __init__.py
│   ├── board.py         # Board representation, move validation, win/draw detection
│   ├── heuristic.py     # Pattern-based heuristic evaluation function
│   ├── move_gen.py      # Candidate move generation (near existing stones)
│   ├── search.py        # Minimax algorithm with Alpha-Beta pruning
│   └── game.py          # Human-vs-AI game loop interface
├── tests/               # Unit tests
│   ├── __init__.py
│   ├── test_board.py
│   ├── test_heuristic.py
│   ├── test_move_gen.py
│   └── test_search.py
├── main.py              # Entry point
├── requirements.txt     # Runtime + development dependencies
└── pyproject.toml       # Project metadata and tooling configuration
```

## Setup

**Prerequisites:** Python 3.10 or newer.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Running Tests

```bash
pytest
```