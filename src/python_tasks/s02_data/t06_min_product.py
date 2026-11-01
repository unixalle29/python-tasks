import sys
from collections.abc import Sequence

MIN_NUMBERS = 2


def parse_integers(raw: str) -> list[int]:
    tokens = raw.split()
    if len(tokens) < MIN_NUMBERS:
        raise ValueError("at least two integers are required")
    try:
        return [int(token) for token in tokens]
    except ValueError as exc:
        raise ValueError("all values must be integers") from exc


def min_product_pair(numbers: Sequence[int]) -> tuple[int, int, int]:
    if len(numbers) < MIN_NUMBERS:
        raise ValueError("at least two integers are required")
    ordered = sorted(numbers)
    candidates = (
        (ordered[0], ordered[1]),
        (ordered[0], ordered[-1]),
        (ordered[-2], ordered[-1]),
    )
    first, second = min(candidates, key=lambda pair: pair[0] * pair[1])
    return first, second, first * second


def main() -> None:
    try:
        numbers = parse_integers(sys.stdin.read())
        first, second, product = min_product_pair(numbers)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    print(first, second, product)


if __name__ == "__main__":
    main()
