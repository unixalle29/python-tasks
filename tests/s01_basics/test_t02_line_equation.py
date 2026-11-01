import pytest

from python_tasks.s01_basics.t02_line_equation import line_coefficients, main, parse_coordinates


@pytest.mark.parametrize(
    ("points", "expected"),
    [
        pytest.param((0, 0, 1, 1), (1, 0), id="slope-one"),
        pytest.param((0, 1, 1, 3), (2, 1), id="slope-two"),
        pytest.param((0, 5, 10, 5), (0, 5), id="horizontal"),
        pytest.param((-1, -1, 1, 1), (1, 0), id="negative-coordinates"),
        pytest.param((0, 0, 3, 1), (1 / 3, 0), id="fractional-slope"),
        pytest.param((0, 5, 5, 0), (-1, 5), id="negative-slope"),
        pytest.param((1.5, 2.5, 3.5, 4.5), (1, 1), id="fractional-coordinates"),
    ],
)
def test_line_coefficients(points: tuple[float, ...], expected: tuple[float, float]) -> None:
    assert line_coefficients(*points) == pytest.approx(expected)


@pytest.mark.parametrize(
    "points",
    [
        pytest.param((1, 2, 1, 5), id="vertical"),
        pytest.param((2, 3, 2, 3), id="coincident"),
    ],
)
def test_line_coefficients_rejects_degenerate_points(points: tuple[float, ...]) -> None:
    with pytest.raises(ValueError):
        line_coefficients(*points)


def test_line_coefficients_rejects_unrepresentable_result() -> None:
    with pytest.raises(ValueError):
        line_coefficients(0.0, 0.0, 5e-324, 1e308)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param("0 0 1 1", (0.0, 0.0, 1.0, 1.0), id="integers"),
        pytest.param(" 1.5 -2 3.5 4 ", (1.5, -2.0, 3.5, 4.0), id="decimals-and-whitespace"),
        pytest.param("1e2 -2.5e-1 3 4", (100.0, -0.25, 3.0, 4.0), id="scientific-notation"),
    ],
)
def test_parse_coordinates_valid(raw: str, expected: tuple[float, ...]) -> None:
    assert parse_coordinates(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        pytest.param("", id="empty"),
        pytest.param("0 0 1", id="too-few"),
        pytest.param("0 0 1 1 2", id="too-many"),
        pytest.param("a b c d", id="text"),
        pytest.param("nan 0 1 1", id="nan"),
        pytest.param("0 inf 1 1", id="positive-infinity"),
        pytest.param("0 0 -inf 1", id="negative-infinity"),
    ],
)
def test_parse_coordinates_rejects_invalid_input(raw: str) -> None:
    with pytest.raises(ValueError):
        parse_coordinates(raw)


@pytest.mark.parametrize(
    ("stdin", "expected"),
    [
        pytest.param("0 0 1 1\n", (1.0, 0.0), id="slope-one"),
        pytest.param("0 5 10 5\n", (0.0, 5.0), id="horizontal"),
    ],
)
def test_cli_output(run_cli, stdin: str, expected: tuple[float, float]) -> None:
    code, out, err = run_cli(main, stdin)
    assert code is None
    assert err == ""
    assert tuple(map(float, out.split())) == pytest.approx(expected)


@pytest.mark.parametrize(
    "stdin",
    [
        pytest.param("", id="empty"),
        pytest.param("0 0 1\n", id="too-few"),
        pytest.param("0 0 1 1 2\n", id="too-many"),
        pytest.param("a b c d\n", id="text"),
        pytest.param("1 2 1 5\n", id="vertical"),
        pytest.param("nan 0 1 1\n", id="nan"),
    ],
)
def test_cli_rejects_invalid_input(assert_cli_error, stdin: str) -> None:
    assert_cli_error(main, stdin)
