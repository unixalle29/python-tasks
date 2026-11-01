from collections.abc import Callable

import pytest

from python_tasks.s01_basics.t05_minimum import main, minimize

EPSILON = 0.01


@pytest.mark.parametrize(
    ("function", "expected"),
    [
        pytest.param(lambda value: 2 * value**2 + 3 * value + 1, -0.75, id="quadratic"),
        pytest.param(lambda value: (value - 1) ** 2, 1.0, id="shifted-parabola"),
        pytest.param(lambda value: value, -4.0, id="left-boundary"),
        pytest.param(lambda value: -value, 2.0, id="right-boundary"),
    ],
)
def test_minimize(function: Callable[[float], float], expected: float) -> None:
    assert minimize(function, -4, 2) == pytest.approx(expected, abs=EPSILON)


def test_minimize_constant_function_returns_point_inside_interval() -> None:
    x = minimize(lambda _: 42, -4, 2)
    assert -4 <= x <= 2


def test_minimize_with_custom_epsilon() -> None:
    x = minimize(lambda value: (value - 1) ** 2, -4, 2, 1e-9)
    assert x == pytest.approx(1, abs=1e-9)


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("inf"), id="positive-infinity"),
        pytest.param(float("-inf"), id="negative-infinity"),
    ],
)
def test_minimize_rejects_non_finite_bounds_and_epsilon(value: float) -> None:
    with pytest.raises(ValueError):
        minimize(lambda x: x, value, 2)
    with pytest.raises(ValueError):
        minimize(lambda x: x, -4, value)
    with pytest.raises(ValueError):
        minimize(lambda x: x, -4, 2, value)


@pytest.mark.parametrize(
    ("left", "right"),
    [
        pytest.param(0, 0, id="empty"),
        pytest.param(1, -1, id="reversed"),
        pytest.param(2, 1, id="reversed-close"),
    ],
)
def test_minimize_rejects_invalid_interval(left: float, right: float) -> None:
    with pytest.raises(ValueError):
        minimize(lambda x: x, left, right)


@pytest.mark.parametrize(
    "epsilon",
    [
        pytest.param(0, id="zero"),
        pytest.param(-0.01, id="small-negative"),
        pytest.param(-1, id="negative"),
    ],
)
def test_minimize_rejects_non_positive_epsilon(epsilon: float) -> None:
    with pytest.raises(ValueError):
        minimize(lambda x: x, -4, 2, epsilon)


@pytest.mark.parametrize(
    "result",
    [
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("inf"), id="positive-infinity"),
        pytest.param(float("-inf"), id="negative-infinity"),
    ],
)
def test_minimize_rejects_non_finite_function_values(result: float) -> None:
    with pytest.raises(ValueError):
        minimize(lambda _: result, -4, 2)


@pytest.mark.parametrize(
    ("left", "right"),
    [
        pytest.param(-4, 2, id="wide-interval"),
        pytest.param(0, 0.001, id="tiny-interval"),
    ],
)
def test_minimize_rejects_non_callable(left: float, right: float) -> None:
    with pytest.raises(TypeError):
        minimize(None, left, right)


def test_cli_output(run_cli) -> None:
    code, out, err = run_cli(main, "")
    assert code is None
    assert err == ""
    assert float(out) == pytest.approx(-0.75, abs=EPSILON)
