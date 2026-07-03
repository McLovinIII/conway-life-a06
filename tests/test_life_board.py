import pytest
from src.life_board import LifeBoard


def live_cells(board):
    return set(board.alive)


def test_empty_board_remains_empty():
    board = LifeBoard(5, 5)
    board.step()
    assert board.alive == set()
    assert board.generation == 1


def test_underpopulation_cell_dies():
    board = LifeBoard(5, 5, {(2, 2)})
    board.step()
    assert not board.is_alive(2, 2)


def test_blinker_oscillates():
    board = LifeBoard(5, 5, {(2, 1), (2, 2), (2, 3)})
    board.step()
    assert live_cells(board) == {(1, 2), (2, 2), (3, 2)}
    board.step()
    assert live_cells(board) == {(2, 1), (2, 2), (2, 3)}


def test_block_is_stable():
    board = LifeBoard(6, 6, {(2, 2), (2, 3), (3, 2), (3, 3)})
    board.step()
    assert live_cells(board) == {(2, 2), (2, 3), (3, 2), (3, 3)}


def test_reproduction_with_three_neighbours():
    board = LifeBoard(5, 5, {(1, 2), (2, 1), (2, 3)})
    board.step()
    assert board.is_alive(2, 2)


def test_toggle_cell():
    board = LifeBoard(3, 3)
    board.toggle(1, 1)
    assert board.is_alive(1, 1)
    board.toggle(1, 1)
    assert not board.is_alive(1, 1)


def test_invalid_size_rejected():
    with pytest.raises(ValueError):
        LifeBoard(0, 5)


def test_out_of_bounds_rejected():
    board = LifeBoard(3, 3)
    with pytest.raises(ValueError):
        board.set_alive(4, 0)
