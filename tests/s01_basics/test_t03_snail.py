import pytest

from python_tasks.s01_basics.t03_snail import days_to_top, main, parse_arguments


@pytest.mark.parametrize(
    ("height", "climb", "slide", "expected"),
    [
        pytest.param(10, 3, 2, 8, id="classic"),
        pytest.param(5, 3, 2, 3, id="short-pole"),
        pytest.param(4, 3, 1, 2, id="two-days"),
        pytest.param(10, 5, 3, 4, id="four-days"),
        pytest.param(6, 3, 1, 3, id="unit-slide"),
        pytest.param(1, 1, 1, 1, id="height-one"),
        pytest.param(5, 5, 10, 1, id="large-slide"),
        pytest.param(5, 10, 1, 1, id="climb-exceeds-height"),
        pytest.param(100, 100, 1, 1, id="climb-equals-height"),
    ],
)
def test_days_to_top(height: int, climb: int, slide: int, expected: int) -> None:
    assert days_to_top(height, climb, slide) == expected


@pytest.mark.parametrize(
    ("height", "climb", "slide"),
    [
        pytest.param(10, 2, 2, id="equal-climb-and-slide"),
        pytest.param(2, 1, 1, id="equal-on-short-pole"),
        pytest.param(10, 1, 2, id="slide-exceeds-climb"),
    ],
)
def test_days_to_top_rejects_impossible_climb(height: int, climb: int, slide: int) -> None:
    with pytest.raises(ValueError):
        days_to_top(height, climb, slide)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param("10 3 2", (10, 3, 2), id="integers"),
        pytest.param(" 4 3 1 ", (4, 3, 1), id="whitespace"),
        pytest.param("01 2 3", (1, 2, 3), id="leading-zeros"),
        pytest.param("+5 +3 +2", (5, 3, 2), id="plus-signs"),
    ],
)
def test_parse_arguments_valid(raw: str, expected: tuple[int, int, int]) -> None:
    assert parse_arguments(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        pytest.param("", id="empty"),
        pytest.param("10 3", id="too-few"),
        pytest.param("10 3 2 1", id="too-many"),
        pytest.param("a 3 2", id="text"),
        pytest.param("10 2.5 1", id="float"),
        pytest.param("0 1 1", id="zero-height"),
        pytest.param("-1 1 1", id="negative-height"),
        pytest.param("1 0 1", id="zero-climb"),
        pytest.param("1 -1 1", id="negative-climb"),
        pytest.param("1 1 0", id="zero-slide"),
        pytest.param("1 1 -1", id="negative-slide"),
    ],
)
def test_parse_arguments_rejects_invalid_input(raw: str) -> None:
    with pytest.raises(ValueError):
        parse_arguments(raw)


def _simulate(height: int, climb: int, slide: int) -> int:
    position = 0
    day = 0
    while position < height:
        day += 1
        position += climb
        if position >= height:
            return day
        position -= slide
    raise AssertionError


@pytest.mark.parametrize(
    ("height", "climb", "slide"),
    [
        pytest.param(10, 3, 2, id="classic"),
        pytest.param(5, 3, 2, id="short-pole"),
        pytest.param(6, 3, 1, id="unit-slide"),
        pytest.param(100, 7, 4, id="long-pole"),
        pytest.param(1000, 13, 5, id="very-long-pole"),
    ],
)
def test_days_to_top_matches_simulation(height: int, climb: int, slide: int) -> None:
    assert days_to_top(height, climb, slide) == _simulate(height, climb, slide)


@pytest.mark.parametrize(
    ("stdin", "expected"),
    [
        pytest.param("10 3 2\n", "8", id="classic"),
        pytest.param("4 3 1\n", "2", id="two-days"),
        pytest.param("1 1 100\n", "1", id="first-day"),
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
        pytest.param("10 3\n", id="too-few"),
        pytest.param("10 3 2 1\n", id="too-many"),
        pytest.param("a 3 2\n", id="text"),
        pytest.param("10 2 2\n", id="impossible-climb"),
        pytest.param("10 -3 2\n", id="negative"),
        pytest.param("0 1 1\n", id="zero-height"),
    ],
)
def test_cli_rejects_invalid_input(assert_cli_error, stdin: str) -> None:
    assert_cli_error(main, stdin)
