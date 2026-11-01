import ast
import sys

from PyQt6.QtWidgets import QApplication, QGridLayout, QLineEdit, QPushButton, QWidget

BUTTONS = ("7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "C", "+")


def evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd | ast.USub):
        value = evaluate(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value
    if isinstance(node, ast.BinOp):
        left = evaluate(node.left)
        right = evaluate(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            if right == 0:
                raise ValueError("division by zero")
            return left / right
    raise ValueError("unsupported expression")


def calculate(expression: str) -> float:
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("invalid expression") from exc
    return evaluate(tree.body)


class Calculator(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Калькулятор")
        self.expression = ""
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        layout = QGridLayout(self)
        layout.addWidget(self.display, 0, 0, 1, 4)
        for index, label in enumerate(BUTTONS):
            button = QPushButton(label)
            button.clicked.connect(lambda _checked, text=label: self.press(text))
            layout.addWidget(button, index // 4 + 1, index % 4)
        equals = QPushButton("=")
        equals.clicked.connect(self.calculate)
        layout.addWidget(equals, len(BUTTONS) // 4 + 1, 0, 1, 4)

    def press(self, label: str) -> None:
        if label == "C":
            self.expression = ""
        else:
            self.expression += label
        self.display.setText(self.expression)

    def calculate(self) -> None:
        try:
            result = calculate(self.expression)
        except ValueError as exc:
            self.display.setText(f"Ошибка: {exc}")
            return
        self.expression = str(result)
        self.display.setText(self.expression)


def main() -> None:
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
