import pytest

from python_tasks.s02_data.t06_min_product import main, min_product_pair, parse_integers


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param("1 2 3", [1, 2, 3], id="positive"),
        pytest.param("-5 -4 0 1", [-5, -4, 0, 1], id="negative"),
        pytest.param(" 4   5 ", [4, 5], id="whitespace"),
        pytest.param("+5 -3", [5, -3], id="plus-sign"),
    ],
)
def test_parse_integers_valid(raw: str, expected: list[int]) -> None:
    assert parse_integers(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        pytest.param("", id="empty"),
        pytest.param("1", id="single-value"),
        pytest.param("1 2.5", id="float"),
        pytest.param("a b", id="text"),
        pytest.param("1 extra", id="mixed"),
    ],
)
def test_parse_integers_rejects_invalid_input(raw: str) -> None:
    with pytest.raises(ValueError):
        parse_integers(raw)


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([1, 2, 3], (1, 2, 2), id="positive"),
        pytest.param([-5, -4, 0, 1], (-5, 1, -5), id="negative-with-zero"),
        pytest.param([-10, -9, 1, 2], (-10, 2, -20), id="large-negative"),
        pytest.param([-10, -9, -8, -7], (-8, -7, 56), id="all-negative"),
        pytest.param([0, 0, 0], (0, 0, 0), id="all-zero"),
        pytest.param([5, 5], (5, 5, 25), id="duplicates"),
        pytest.param([3, -3], (-3, 3, -9), id="two-numbers"),
        pytest.param([1, 0, -1], (-1, 1, -1), id="with-zero"),
    ],
)
def test_min_product_pair(numbers: list[int], expected: tuple[int, int, int]) -> None:
    assert min_product_pair(numbers) == expected


@pytest.mark.parametrize(
    "numbers",
    [
        pytest.param([], id="empty"),
        pytest.param([1], id="single"),
    ],
)
def test_min_product_pair_rejects_too_few_values(numbers: list[int]) -> None:
    with pytest.raises(ValueError):
        min_product_pair(numbers)


def test_min_product_matches_brute_force() -> None:
    numbers = [-7, -3, 0, 2, 5, 9]
    expected = min(first * second for index, first in enumerate(numbers) for second in numbers[index + 1 :])
    assert min_product_pair(numbers)[2] == expected


@pytest.mark.parametrize(
    ("stdin", "expected"),
    [
        pytest.param("1 2 3\n", "1 2 2", id="positive"),
        pytest.param("-5 -4 0 1\n", "-5 1 -5", id="negative"),
    ],
)
def test_cli_output(run_cli, stdin: str, expected: str) -> None:
    code, out, err = run_cli(main, stdin)
    assert code is None
    assert out.strip() == expected
    assert err == ""


@pytest.mark.parametrize(
    "stdin",
    [
        pytest.param("", id="empty"),
        pytest.param("1\n", id="single-value"),
        pytest.param("1 2.5\n", id="float"),
        pytest.param("a b\n", id="text"),
    ],
)
def test_cli_rejects_invalid_input(assert_cli_error, stdin: str) -> None:
    assert_cli_error(main, stdin)
