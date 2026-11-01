import sys

from PyQt6.QtWidgets import QApplication, QGridLayout, QLabel, QPushButton, QWidget

SIZE = 10
LETTERS = "АБВГДЕЖЗИК"


class Board:
    def __init__(self, size: int = SIZE) -> None:
        self.size = size
        self.ships: set[tuple[int, int]] = set()

    def can_place(self, row: int, col: int, length: int = 1, horizontal: bool = True) -> bool:
        if length < 1:
            return False
        for offset in range(length):
            current_row = row if horizontal else row + offset
            current_col = col + offset if horizontal else col
            if not (0 <= current_row < self.size and 0 <= current_col < self.size):
                return False
            for row_shift in (-1, 0, 1):
                for col_shift in (-1, 0, 1):
                    neighbour = (current_row + row_shift, current_col + col_shift)
                    if neighbour in self.ships:
                        return False
        return True

    def place_ship(self, row: int, col: int, length: int = 1, horizontal: bool = True) -> bool:
        if not self.can_place(row, col, length, horizontal):
            return False
        for offset in range(length):
            current_row = row if horizontal else row + offset
            current_col = col + offset if horizontal else col
            self.ships.add((current_row, current_col))
        return True


class SeaBattleWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Морской бой")
        self.board = Board()
        self.buttons: dict[tuple[int, int], QPushButton] = {}
        layout = QGridLayout(self)
        for col, letter in enumerate(LETTERS):
            layout.addWidget(QLabel(letter), 0, col + 1)
        for row in range(SIZE):
            layout.addWidget(QLabel(str(row + 1)), row + 1, 0)
            for col in range(SIZE):
                button = QPushButton()
                button.setFixedSize(30, 30)
                button.clicked.connect(lambda _checked, r=row, c=col: self.place(r, c))
                layout.addWidget(button, row + 1, col + 1)
                self.buttons[(row, col)] = button
        self.status = QLabel("Щёлкните по полю")
        layout.addWidget(self.status, SIZE + 1, 0, 1, SIZE + 1)

    def place(self, row: int, col: int) -> None:
        if self.board.place_ship(row, col):
            self.buttons[(row, col)].setText("■")
            self.status.setText("Корабль поставлен")
        else:
            self.status.setText("Здесь нельзя ставить корабль")


def main() -> None:
    app = QApplication(sys.argv)
    window = SeaBattleWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
