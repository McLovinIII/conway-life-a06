from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class LifeBoard:
    """Конечное клеточное поле для автомата Conway's Game of Life."""

    rows: int = 30
    cols: int = 40
    alive: set[tuple[int, int]] = field(default_factory=set)
    generation: int = 0

    def __post_init__(self) -> None:
        if self.rows <= 0 or self.cols <= 0:
            raise ValueError("Размер поля должен быть положительным")
        self.alive = {cell for cell in self.alive if self.in_bounds(*cell)}

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_alive(self, row: int, col: int) -> bool:
        return (row, col) in self.alive

    def set_alive(self, row: int, col: int, value: bool = True) -> None:
        if not self.in_bounds(row, col):
            raise ValueError("Координаты клетки выходят за границы поля")
        if value:
            self.alive.add((row, col))
        else:
            self.alive.discard((row, col))

    def toggle(self, row: int, col: int) -> None:
        self.set_alive(row, col, not self.is_alive(row, col))

    def clear(self) -> None:
        self.alive.clear()
        self.generation = 0

    def neighbor_count(self, row: int, col: int) -> int:
        return sum(
            (row + dr, col + dc) in self.alive
            for dr in (-1, 0, 1)
            for dc in (-1, 0, 1)
            if not (dr == 0 and dc == 0)
            and self.in_bounds(row + dr, col + dc)
        )

    def step(self) -> None:
        candidates: set[tuple[int, int]] = set(self.alive)
        for row, col in list(self.alive):
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr or dc:
                        nr, nc = row + dr, col + dc
                        if self.in_bounds(nr, nc):
                            candidates.add((nr, nc))

        next_alive: set[tuple[int, int]] = set()
        for row, col in candidates:
            neighbours = self.neighbor_count(row, col)
            if neighbours == 3 or (self.is_alive(row, col) and neighbours == 2):
                next_alive.add((row, col))
        self.alive = next_alive
        self.generation += 1

    def load_cells(self, cells: Iterable[tuple[int, int]]) -> None:
        self.alive = set()
        for row, col in cells:
            if self.in_bounds(row, col):
                self.alive.add((row, col))
        self.generation = 0
