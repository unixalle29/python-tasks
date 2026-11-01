import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QTextEdit


class TextEditor(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Редактор")
        self.resize(600, 400)
        self.editor = QTextEdit(self)
        self.setCentralWidget(self.editor)
        menu = self.menuBar().addMenu("Файл")
        menu.addAction("Открыть", self.open_dialog)
        menu.addAction("Сохранить", self.save_dialog)

    def open_file(self, path: Path) -> None:
        self.editor.setPlainText(path.read_text(encoding="utf-8"))

    def save_file(self, path: Path) -> None:
        path.write_text(self.editor.toPlainText(), encoding="utf-8")

    def open_dialog(self) -> None:
        name, _ = QFileDialog.getOpenFileName(self, "Открыть файл")
        if name:
            self.open_file(Path(name))

    def save_dialog(self) -> None:
        name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл")
        if name:
            self.save_file(Path(name))


def main() -> None:
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
