import pytest

from python_tasks.s01_basics.t06_ascii_digits import main, parse_number, render_number

EXPECTED_ZERO = "***\n* *\n* *\n* *\n***"
EXPECTED_MINUS_ONE = "     * \n    ** \n***  * \n     * \n    ***"


@pytest.mark.parametrize("digit", range(10))
def test_digit_render_shape(digit: int) -> None:
    lines = render_number(digit).splitlines()
    assert len(lines) == 5
    assert all(len(line) == 3 for line in lines)
    assert all(set(line) <= {"*", " "} for line in lines)


def test_zero_rendering() -> None:
    assert render_number(0) == EXPECTED_ZERO


def test_multi_digit_rendering() -> None:
    lines = render_number(2024).splitlines()
    assert len(lines) == 5
    assert all(len(line) == 4 * 3 + 3 for line in lines)


def test_negative_rendering() -> None:
    assert render_number(-1) == EXPECTED_MINUS_ONE


def test_negative_zero_rendering() -> None:
    assert render_number(-0) == EXPECTED_ZERO


def test_large_number_rendering() -> None:
    lines = render_number(1234567890).splitlines()
    assert len(lines) == 5
    assert all(len(line) == 10 * 3 + 9 for line in lines)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param("42", 42, id="plain"),
        pytest.param(" 42 ", 42, id="whitespace"),
        pytest.param("-1", -1, id="negative"),
        pytest.param("+7", 7, id="plus-sign"),
        pytest.param("0007", 7, id="leading-zeros"),
    ],
)
def test_parse_number_valid(raw: str, expected: int) -> None:
    assert parse_number(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        pytest.param("", id="empty"),
        pytest.param(" \n ", id="whitespace-only"),
        pytest.param("abc", id="text"),
        pytest.param("1.5", id="float"),
        pytest.param("1 2", id="extra-token"),
        pytest.param("1" * 5000, id="too-many-digits"),
    ],
)
def test_parse_number_rejects_invalid_input(raw: str) -> None:
    with pytest.raises(ValueError):
        parse_number(raw)


@pytest.mark.parametrize(
    ("stdin", "expected"),
    [
        pytest.param("0\n", EXPECTED_ZERO, id="zero"),
        pytest.param("-1\n", EXPECTED_MINUS_ONE, id="negative"),
    ],
)
def test_cli_output(run_cli, stdin: str, expected: str) -> None:
    code, out, err = run_cli(main, stdin)
    assert code is None
    assert out.rstrip("\n") == expected
    assert err == ""


@pytest.mark.parametrize(
    "stdin",
    [
        pytest.param("", id="empty"),
        pytest.param("\n", id="newline-only"),
        pytest.param("abc\n", id="text"),
        pytest.param("1.5\n", id="float"),
        pytest.param("1 2\n", id="extra-token"),
        pytest.param("1" * 5000 + "\n", id="too-many-digits"),
    ],
)
def test_cli_rejects_invalid_input(assert_cli_error, stdin: str) -> None:
    assert_cli_error(main, stdin)
