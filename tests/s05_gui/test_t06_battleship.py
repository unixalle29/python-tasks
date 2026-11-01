import pytest

from python_tasks.s05_gui.t06_battleship import Board, SeaBattleWindow


def test_place_single_ship() -> None:
    board = Board()
    assert board.place_ship(0, 0)
    assert board.ships == {(0, 0)}


@pytest.mark.parametrize(
    ("row", "col"),
    [(0, 1), (1, 0), (1, 1), (0, 0)],
)
def test_cannot_place_adjacent_overlapping_or_diagonal_ship(row: int, col: int) -> None:
    board = Board()
    board.place_ship(0, 0)
    assert not board.place_ship(row, col)


def test_place_horizontal_and_vertical_ship() -> None:
    board = Board()
    assert board.place_ship(2, 2, length=3, horizontal=True)
    assert board.ships == {(2, 2), (2, 3), (2, 4)}
    assert board.place_ship(5, 5, length=3, horizontal=False)
    assert board.ships == {(2, 2), (2, 3), (2, 4), (5, 5), (6, 5), (7, 5)}


@pytest.mark.parametrize(
    ("row", "col", "length", "horizontal"),
    [
        (0, 0, 0, True),
        (0, 9, 2, True),
        (9, 0, 2, False),
        (-1, 0, 1, True),
        (0, -1, 1, True),
    ],
)
def test_rejects_invalid_ship_placement(row: int, col: int, length: int, horizontal: bool) -> None:
    board = Board()
    assert not board.place_ship(row, col, length, horizontal)


def test_window_places_ship_on_click(qtbot) -> None:
    window = SeaBattleWindow()
    qtbot.addWidget(window)
    window.place(0, 0)
    assert window.board.ships == {(0, 0)}
    assert window.buttons[(0, 0)].text() == "■"
    window.place(0, 1)
    assert window.status.text() == "Здесь нельзя ставить корабль"
