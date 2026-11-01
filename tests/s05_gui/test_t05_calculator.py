import pytest
from PyQt6.QtWidgets import QPushButton

from python_tasks.s05_gui.t05_calculator import Calculator, calculate


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1+2", 3),
        ("2*3+4", 10),
        ("(2+3)*4", 20),
        ("-5+2", -3),
        ("7/2", 3.5),
    ],
)
def test_calculate(expression: str, expected: float) -> None:
    assert calculate(expression) == pytest.approx(expected)


@pytest.mark.parametrize("expression", ["", "1+", "2**3", "abc", "1/0"])
def test_calculate_rejects_invalid_expression(expression: str) -> None:
    with pytest.raises(ValueError):
        calculate(expression)


def find_button(calculator: Calculator, text: str) -> QPushButton:
    return next(button for button in calculator.findChildren(QPushButton) if button.text() == text)


def test_gui_builds_and_evaluates_expression(qtbot) -> None:
    calculator = Calculator()
    qtbot.addWidget(calculator)
    for text in ("2", "+", "3"):
        find_button(calculator, text).click()
    find_button(calculator, "=").click()
    assert calculator.display.text() == "5.0"


def test_gui_clear_button(qtbot) -> None:
    calculator = Calculator()
    qtbot.addWidget(calculator)
    find_button(calculator, "1").click()
    find_button(calculator, "C").click()
    assert calculator.display.text() == ""
