import random

import pytest

from python_tasks.s02_data.t07_frequencies import (
    MAX_VALUE,
    MIN_VALUE,
    SEQUENCE_LENGTH,
    count_frequencies,
    generate_frequencies,
    main,
)


@pytest.mark.parametrize(
    ("values", "maximum", "expected"),
    [
        pytest.param([1, 2, 2, 3], 3, [(2, 2), (1, 1), (3, 1)], id="basic"),
        pytest.param([1], 3, [(1, 1), (2, 0), (3, 0)], id="includes-missing-numbers"),
        pytest.param([3, 1, 3, 2], 3, [(3, 2), (1, 1), (2, 1)], id="ties-sorted-by-number"),
        pytest.param([], 3, [(1, 0), (2, 0), (3, 0)], id="empty-values"),
        pytest.param(
            [5, 5],
            5,
            [(5, 2), (1, 0), (2, 0), (3, 0), (4, 0)],
            id="maximum-five",
        ),
    ],
)
def test_count_frequencies(
    values: list[int],
    maximum: int,
    expected: list[tuple[int, int]],
) -> None:
    assert count_frequencies(values, maximum) == expected


@pytest.mark.parametrize(
    "maximum",
    [
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_count_frequencies_rejects_non_positive_maximum(maximum: int) -> None:
    with pytest.raises(ValueError):
        count_frequencies([], maximum)


@pytest.mark.parametrize(
    "values",
    [
        pytest.param([0], id="below-range"),
        pytest.param([6], id="above-range"),
        pytest.param([-1], id="negative"),
    ],
)
def test_count_frequencies_rejects_out_of_range_values(values: list[int]) -> None:
    with pytest.raises(ValueError):
        count_frequencies(values, 5)


@pytest.mark.parametrize("seed", [0, 1, 42])
def test_generate_frequencies(seed: int) -> None:
    table = generate_frequencies(1000, random.Random(seed), maximum=5)
    assert {number for number, _ in table} == {1, 2, 3, 4, 5}
    assert sum(count for _, count in table) == 1000
    assert table == sorted(table, key=lambda item: (-item[1], item[0]))


def test_generate_frequencies_is_deterministic() -> None:
    assert generate_frequencies(100, random.Random(42), maximum=5) == generate_frequencies(
        100,
        random.Random(42),
        maximum=5,
    )


def test_generate_frequencies_with_zero_count() -> None:
    assert generate_frequencies(0, random.Random(0), maximum=3) == [(1, 0), (2, 0), (3, 0)]


@pytest.mark.parametrize(
    "count",
    [
        pytest.param(-1, id="negative"),
    ],
)
def test_generate_frequencies_rejects_negative_count(count: int) -> None:
    with pytest.raises(ValueError):
        generate_frequencies(count, random.Random(0), maximum=5)


@pytest.mark.parametrize(
    "maximum",
    [
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_generate_frequencies_rejects_non_positive_maximum(maximum: int) -> None:
    with pytest.raises(ValueError):
        generate_frequencies(10, random.Random(0), maximum=maximum)


def test_cli_output(run_cli) -> None:
    code, out, err = run_cli(main, "")
    assert code is None
    assert err == ""
    table = []
    for line in out.strip().splitlines():
        number, count = line.split(": ")
        table.append((int(number), int(count)))
    assert len(table) == MAX_VALUE
    assert {number for number, _ in table} == set(range(MIN_VALUE, MAX_VALUE + 1))
    assert sum(count for _, count in table) == SEQUENCE_LENGTH
    assert table == sorted(table, key=lambda item: (-item[1], item[0]))
