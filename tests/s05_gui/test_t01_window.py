from PyQt6.QtCore import Qt

from python_tasks.s05_gui.t01_window import MainWindow


def test_window_has_label_and_button(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.label.text() == "Привет, мир!"
    assert window.label.alignment() == Qt.AlignmentFlag.AlignCenter
    assert window.button.text() == "Сменить цвет"


def test_button_changes_color(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.button.click()
    assert window.label.styleSheet() == "color: green;"
    window.button.click()
    assert window.label.styleSheet() == "color: blue;"
    window.button.click()
    assert window.label.styleSheet() == "color: red;"
    window.button.click()
    assert window.label.styleSheet() == "color: green;"
