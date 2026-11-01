import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

COLORS = ("red", "green", "blue")


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Python")
        self.color_index = 0
        self.label = QLabel("Привет, мир!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button = QPushButton("Сменить цвет")
        self.button.clicked.connect(self.change_color)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

    def change_color(self) -> None:
        self.color_index = (self.color_index + 1) % len(COLORS)
        self.label.setStyleSheet(f"color: {COLORS[self.color_index]};")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
