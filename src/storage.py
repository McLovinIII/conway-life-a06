from __future__ import annotations

from pathlib import Path
from .life_board import LifeBoard


def save_life_file(board: LifeBoard, path: str | Path) -> None:
    path = Path(path)
    lines = [f"{board.rows} {board.cols}"]
    for row in range(board.rows):
        lines.append("".join("#" if board.is_alive(row, col) else "." for col in range(board.cols)))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_life_file(path: str | Path) -> LifeBoard:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    if not lines:
        raise ValueError("Файл состояния пуст")
    try:
        rows, cols = map(int, lines[0].split())
    except ValueError as exc:
        raise ValueError("Первая строка должна содержать два размера поля") from exc
    if len(lines[1:]) != rows:
        raise ValueError("Число строк поля не совпадает с указанной высотой")
    board = LifeBoard(rows, cols)
    for row, line in enumerate(lines[1:]):
        if len(line) != cols or any(char not in '.#' for char in line):
            raise ValueError("Поле содержит недопустимые символы")
        for col, char in enumerate(line):
            if char == '#':
                board.set_alive(row, col)
    return board
