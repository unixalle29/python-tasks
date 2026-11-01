import pytest

from python_tasks.s01_basics.t01_leap_year import is_leap_year, main, parse_year


@pytest.mark.parametrize(
    ("year", "expected"),
    [
        pytest.param(4, True, id="divisible-by-4"),
        pytest.param(400, True, id="divisible-by-400"),
        pytest.param(1600, True, id="divisible-by-400-early"),
        pytest.param(2000, True, id="divisible-by-400-modern"),
        pytest.param(2024, True, id="leap-year"),
        pytest.param(2400, True, id="divisible-by-400-future"),
        pytest.param(9996, True, id="large-leap-year"),
        pytest.param(1, False, id="year-one"),
        pytest.param(2, False, id="year-two"),
        pytest.param(3, False, id="year-three"),
        pytest.param(100, False, id="century"),
        pytest.param(200, False, id="century-200"),
        pytest.param(1900, False, id="century-not-400"),
        pytest.param(2100, False, id="century-not-400-future"),
        pytest.param(2023, False, id="common-year"),
        pytest.param(9999, False, id="large-common-year"),
    ],
)
def test_is_leap_year(year: int, expected: bool) -> None:
    assert is_leap_year(year) is expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param("2024", 2024, id="plain"),
        pytest.param(" 2024 ", 2024, id="whitespace"),
        pytest.param("+2024", 2024, id="plus-sign"),
        pytest.param("0004", 4, id="leading-zeros"),
        pytest.param("1", 1, id="single-digit"),
    ],
)
def test_parse_year_valid(raw: str, expected: int) -> None:
    assert parse_year(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        pytest.param("", id="empty"),
        pytest.param(" \n ", id="whitespace-only"),
        pytest.param("abc", id="text"),
        pytest.param("2024.0", id="float"),
        pytest.param("2024 extra", id="extra-token"),
        pytest.param("0", id="zero"),
        pytest.param("-4", id="negative"),
        pytest.param("-400", id="negative-century"),
    ],
)
def test_parse_year_rejects_invalid_input(raw: str) -> None:
    with pytest.raises(ValueError):
        parse_year(raw)


@pytest.mark.parametrize(
    ("stdin", "expected"),
    [
        pytest.param("2024\n", "yes", id="leap-year"),
        pytest.param("0004\n", "yes", id="leading-zeros"),
        pytest.param("1900\n", "no", id="century-not-400"),
        pytest.param("2023\n", "no", id="common-year"),
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
        pytest.param("\n", id="newline-only"),
        pytest.param("abc\n", id="text"),
        pytest.param("2024.0\n", id="float"),
        pytest.param("2024 extra\n", id="extra-token"),
        pytest.param("0\n", id="zero"),
        pytest.param("-4\n", id="negative"),
    ],
)
def test_cli_rejects_invalid_input(assert_cli_error, stdin: str) -> None:
    assert_cli_error(main, stdin)
