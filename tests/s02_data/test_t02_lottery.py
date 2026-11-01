import random

import pytest

from python_tasks.s02_data.t02_lottery import (
    FIRST_BLOCK_MAX,
    FIRST_BLOCK_SIZE,
    SECOND_BLOCK_MAX,
    format_ticket,
    generate_ticket,
    main,
)


@pytest.mark.parametrize("seed", [0, 1, 42, 123, 9999])
def test_generate_ticket_properties(seed: int) -> None:
    first_block, second_block = generate_ticket(random.Random(seed))
    assert len(first_block) == FIRST_BLOCK_SIZE
    assert len(set(first_block)) == FIRST_BLOCK_SIZE
    assert tuple(sorted(first_block)) == first_block
    assert all(1 <= number <= FIRST_BLOCK_MAX for number in first_block)
    assert 1 <= second_block <= SECOND_BLOCK_MAX


def test_generate_ticket_is_deterministic() -> None:
    assert generate_ticket(random.Random(42)) == generate_ticket(random.Random(42))


def test_generate_ticket_changes_with_seed() -> None:
    assert generate_ticket(random.Random(1)) != generate_ticket(random.Random(2))


@pytest.mark.parametrize(
    ("ticket", "expected"),
    [
        pytest.param(
            ((1, 5, 9, 12, 20, 25, 35), 7),
            "1 5 9 12 20 25 35 | 7",
            id="full-ticket",
        ),
        pytest.param(((1, 2, 3, 4, 5, 6, 7), 54), "1 2 3 4 5 6 7 | 54", id="boundaries"),
    ],
)
def test_format_ticket(ticket: tuple[tuple[int, ...], int], expected: str) -> None:
    assert format_ticket(ticket) == expected


def test_cli_output(run_cli) -> None:
    code, out, err = run_cli(main, "")
    assert code is None
    assert err == ""
    first_part, second_part = out.strip().split(" | ")
    numbers = [int(number) for number in first_part.split()]
    assert len(numbers) == FIRST_BLOCK_SIZE
    assert numbers == sorted(numbers)
    assert len(set(numbers)) == FIRST_BLOCK_SIZE
    assert all(1 <= number <= FIRST_BLOCK_MAX for number in numbers)
    assert 1 <= int(second_part) <= SECOND_BLOCK_MAX
