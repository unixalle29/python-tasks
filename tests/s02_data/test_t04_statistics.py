import math
import random

import pytest

from python_tasks.s02_data.t04_statistics import (
    LOWER_BOUND,
    UPPER_BOUND,
    generate_values,
    main,
    mean,
    parse_count,
    root_sum_squared_deviations,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param("1", 1, id="one"),
        pytest.param(" 5 ", 5, id="whitespace"),
        pytest.param("+7", 7, id="plus-sign"),
        pytest.param("0003", 3, id="leading-zeros"),
    ],
)
def test_parse_count_valid(raw: str, expected: int) -> None:
    assert parse_count(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        pytest.param("", id="empty"),
        pytest.param("abc", id="text"),
        pytest.param("1.5", id="float"),
        pytest.param("0", id="zero"),
        pytest.param("-1", id="negative"),
        pytest.param("3 4", id="extra-token"),
    ],
)
def test_parse_count_rejects_invalid_input(raw: str) -> None:
    with pytest.raises(ValueError):
        parse_count(raw)


@pytest.mark.parametrize("seed", [0, 1, 42])
def test_generate_values(seed: int) -> None:
    values = generate_values(100, random.Random(seed))
    assert len(values) == 100
    assert all(LOWER_BOUND <= value <= UPPER_BOUND for value in values)


def test_generate_values_is_deterministic() -> None:
    assert generate_values(10, random.Random(42)) == generate_values(10, random.Random(42))


@pytest.mark.parametrize(
    "count",
    [
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_generate_values_rejects_non_positive_count(count: int) -> None:
    with pytest.raises(ValueError):
        generate_values(count, random.Random(0))


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([1.0], 1.0, id="single"),
        pytest.param([0.0, 10.0], 5.0, id="bounds"),
        pytest.param([1.0, 2.0, 3.0], 2.0, id="integers"),
        pytest.param([-1.0, 1.0], 0.0, id="symmetric"),
    ],
)
def test_mean(values: list[float], expected: float) -> None:
    assert mean(values) == pytest.approx(expected)


def test_mean_rejects_empty_values() -> None:
    with pytest.raises(ValueError):
        mean([])


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([1.0], 0.0, id="single"),
        pytest.param([5.0, 5.0, 5.0], 0.0, id="constant"),
        pytest.param([0.0, 10.0], math.sqrt(50.0), id="bounds"),
        pytest.param([1.0, 2.0, 3.0], math.sqrt(2.0), id="integers"),
    ],
)
def test_root_sum_squared_deviations(values: list[float], expected: float) -> None:
    assert root_sum_squared_deviations(values) == pytest.approx(expected)


def test_root_sum_squared_deviations_rejects_empty_values() -> None:
    with pytest.raises(ValueError):
        root_sum_squared_deviations([])


@pytest.mark.parametrize(
    "stdin",
    [
        pytest.param("1\n", id="one"),
        pytest.param("5\n", id="five"),
        pytest.param("100\n", id="hundred"),
    ],
)
def test_cli_output(run_cli, stdin: str) -> None:
    code, out, err = run_cli(main, stdin)
    assert code is None
    assert err == ""
    average, deviation = map(float, out.split())
    assert LOWER_BOUND <= average <= UPPER_BOUND
    assert deviation >= 0


@pytest.mark.parametrize(
    "stdin",
    [
        pytest.param("", id="empty"),
        pytest.param("abc\n", id="text"),
        pytest.param("1.5\n", id="float"),
        pytest.param("0\n", id="zero"),
        pytest.param("-1\n", id="negative"),
        pytest.param("3 4\n", id="extra-token"),
    ],
)
def test_cli_rejects_invalid_input(assert_cli_error, stdin: str) -> None:
    assert_cli_error(main, stdin)
