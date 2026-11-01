import sys
from collections.abc import Callable

DEFAULT_EPSILON = 0.01
LEFT_BOUND = -4.0
RIGHT_BOUND = 2.0
THIRDS = 3.0
NEGATIVE_INFINITY = float("-inf")
POSITIVE_INFINITY = float("inf")


def _is_finite(value: float) -> bool:
    return NEGATIVE_INFINITY < value < POSITIVE_INFINITY


def minimize(
    function: Callable[[float], float],
    left: float,
    right: float,
    epsilon: float = DEFAULT_EPSILON,
) -> float:
    if not callable(function):
        raise TypeError("function must be callable")
    if not _is_finite(left) or not _is_finite(right) or not _is_finite(epsilon):
        raise ValueError("bounds and epsilon must be finite")
    if left >= right:
        raise ValueError("the left bound must be less than the right bound")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    while right - left > epsilon:
        third = (right - left) / THIRDS
        left_third = left + third
        right_third = right - third
        left_value = function(left_third)
        right_value = function(right_third)
        if not _is_finite(left_value) or not _is_finite(right_value):
            raise ValueError("the function returned a non-finite value")
        if left_value < right_value:
            right = right_third
        else:
            left = left_third
    return (left + right) / 2


def objective(x: float) -> float:
    return 2 * x * x + 3 * x + 1


def main() -> None:
    try:
        x = minimize(objective, LEFT_BOUND, RIGHT_BOUND)
    except (TypeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    print(f"{x:.2f}")


if __name__ == "__main__":
    main()
