import pytest

from python_tasks.s02_data.t03_matrices import (
    format_matrix,
    main,
    multiply_numpy,
    multiply_pure,
    parse_matrices,
)


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        pytest.param([[2]], [[3]], [[6]], id="one-by-one"),
        pytest.param(
            [[1, 0], [0, 1]],
            [[5, 6], [7, 8]],
            [[5, 6], [7, 8]],
            id="identity",
        ),
        pytest.param(
            [[1, 2], [3, 4]],
            [[5, 6], [7, 8]],
            [[19, 22], [43, 50]],
            id="two-by-two",
        ),
        pytest.param(
            [[1.5, -2], [0, 3]],
            [[2, 1], [-1, 4]],
            [[5, -6.5], [-3, 12]],
            id="fractions",
        ),
    ],
)
def test_multiply_pure(
    left: list[list[float]],
    right: list[list[float]],
    expected: list[list[float]],
) -> None:
    assert multiply_pure(left, right) == expected


def test_multiply_numpy_matches_pure() -> None:
    left = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    right = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
    assert multiply_numpy(left, right) == multiply_pure(left, right)


@pytest.mark.parametrize(
    ("left", "right"),
    [
        pytest.param([], [[1]], id="empty-left"),
        pytest.param([[1]], [], id="empty-right"),
        pytest.param([[1, 2]], [[1], [2]], id="non-square-left"),
        pytest.param([[1]], [[1, 2]], id="non-square-right"),
        pytest.param([[1]], [[1], [2]], id="size-mismatch"),
        pytest.param([[1, 2], [3]], [[1, 2], [3, 4]], id="ragged"),
    ],
)
def test_multiply_pure_rejects_invalid_matrices(
    left: list[list[float]],
    right: list[list[float]],
) -> None:
    with pytest.raises(ValueError):
        multiply_pure(left, right)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param("1 2 3", ([[2.0]], [[3.0]]), id="one-by-one"),
        pytest.param(
            "2 1 2 3 4 5 6 7 8",
            ([[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]),
            id="two-by-two",
        ),
        pytest.param(
            "2 1.5 -2 0 3 2 1 -1 4",
            ([[1.5, -2.0], [0.0, 3.0]], [[2.0, 1.0], [-1.0, 4.0]]),
            id="fractions",
        ),
    ],
)
def test_parse_matrices_valid(
    raw: str,
    expected: tuple[list[list[float]], list[list[float]]],
) -> None:
    assert parse_matrices(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        pytest.param("", id="empty"),
        pytest.param("2", id="missing-values"),
        pytest.param("a 1 2 3", id="non-integer-size"),
        pytest.param("0", id="zero-size"),
        pytest.param("-1 1", id="negative-size"),
        pytest.param("2 1 2 3", id="too-few"),
        pytest.param("2 1 2 3 4 5 6 7 8 9", id="too-many"),
        pytest.param("2 a b c d e f g h", id="non-numeric"),
        pytest.param("2 nan 0 0 0 0 0 0 0", id="nan"),
    ],
)
def test_parse_matrices_rejects_invalid_input(raw: str) -> None:
    with pytest.raises(ValueError):
        parse_matrices(raw)


def test_format_matrix() -> None:
    assert format_matrix([[1.0, 2.5], [3.0, 4.0]]) == "1 2.5\n3 4"


def test_cli_output(run_cli) -> None:
    code, out, err = run_cli(main, "2 1 2 3 4 5 6 7 8\n")
    assert code is None
    assert err == ""
    assert out.strip() == "19 22\n43 50"


@pytest.mark.parametrize(
    "stdin",
    [
        pytest.param("", id="empty"),
        pytest.param("2 1 2 3\n", id="too-few"),
        pytest.param("a b c d\n", id="text"),
        pytest.param("2 nan 0 0 0 0 0 0 0\n", id="nan"),
        pytest.param("0\n", id="zero-size"),
    ],
)
def test_cli_rejects_invalid_input(assert_cli_error, stdin: str) -> None:
    assert_cli_error(main, stdin)
