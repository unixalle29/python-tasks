import math
import sys
from typing import cast

import numpy as np

Matrix = list[list[float]]


def _split_matrix(values: list[float], size: int, offset: int) -> Matrix:
    return [values[offset + row * size : offset + (row + 1) * size] for row in range(size)]


def parse_matrices(raw: str) -> tuple[Matrix, Matrix]:
    tokens = raw.split()
    if not tokens:
        raise ValueError("input is empty")
    try:
        size = int(tokens[0])
    except ValueError as exc:
        raise ValueError("matrix size must be an integer") from exc
    if size < 1:
        raise ValueError("matrix size must be positive")
    expected = 1 + 2 * size * size
    if len(tokens) != expected:
        raise ValueError(f"expected {expected} values, got {len(tokens)}")
    try:
        values = [float(token) for token in tokens[1:]]
    except ValueError as exc:
        raise ValueError("matrix elements must be numbers") from exc
    if not all(math.isfinite(value) for value in values):
        raise ValueError("matrix elements must be finite")
    block_size = size * size
    return _split_matrix(values, size, 0), _split_matrix(values, size, block_size)


def _validate_matrices(left: Matrix, right: Matrix) -> None:
    if not left or not right:
        raise ValueError("matrices must not be empty")
    if len(left) != len(right):
        raise ValueError("matrices must have the same size")
    size = len(left)
    if any(len(row) != size for row in left) or any(len(row) != size for row in right):
        raise ValueError("matrices must be square")


def multiply_pure(left: Matrix, right: Matrix) -> Matrix:
    _validate_matrices(left, right)
    size = len(left)
    return [
        [sum(left[row][index] * right[index][column] for index in range(size)) for column in range(size)]
        for row in range(size)
    ]


def multiply_numpy(left: Matrix, right: Matrix) -> Matrix:
    _validate_matrices(left, right)
    result = np.asarray(left) @ np.asarray(right)
    return cast("Matrix", result.tolist())


def format_matrix(matrix: Matrix) -> str:
    return "\n".join(" ".join(f"{value:g}" for value in row) for row in matrix)


def main() -> None:
    try:
        left, right = parse_matrices(sys.stdin.read())
        product = multiply_pure(left, right)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    print(format_matrix(product))


if __name__ == "__main__":
    main()
