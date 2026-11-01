import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def rotate_pixmap(pixmap: QPixmap, degrees: int) -> QPixmap:
    return pixmap.transformed(QTransform().rotate(degrees))


class ImageViewer(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Просмотр изображений")
        self.pixmap: QPixmap | None = None
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        open_button = QPushButton("Открыть")
        rotate_90_button = QPushButton("Повернуть на 90°")
        rotate_180_button = QPushButton("Повернуть на 180°")
        open_button.clicked.connect(self.open_dialog)
        rotate_90_button.clicked.connect(lambda: self.rotate(90))
        rotate_180_button.clicked.connect(lambda: self.rotate(180))
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(open_button)
        layout.addWidget(rotate_90_button)
        layout.addWidget(rotate_180_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_image(self, path: Path) -> None:
        pixmap = QPixmap(str(path))
        if pixmap.isNull():
            raise ValueError(f"cannot open image: {path}")
        self.pixmap = pixmap
        self.label.setPixmap(pixmap)

    def rotate(self, degrees: int) -> None:
        if self.pixmap is None:
            return
        self.pixmap = rotate_pixmap(self.pixmap, degrees)
        self.label.setPixmap(self.pixmap)

    def open_dialog(self) -> None:
        name, _ = QFileDialog.getOpenFileName(self, "Открыть изображение")
        if name:
            self.open_image(Path(name))


def main() -> None:
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
